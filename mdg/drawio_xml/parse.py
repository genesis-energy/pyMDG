from typing import List, Tuple, Optional
from lxml import etree

from mdg import generation_fields
from mdg.config import settings
from mdg.uml import (
    # UMLAssociation,
    UMLAssociation, UMLAttribute,
    UMLClass,
    # UMLEnumeration,
    UMLInstance,
    UMLPackage,
)


def parse_uml() -> Tuple[UMLPackage, List[UMLInstance]]:
    test_cases: List[UMLInstance] = []

    # Parse into etree and grab root package
    root = etree.parse(settings['source']).getroot()
    model = root.find('./diagram/mxGraphModel/root')
    if model is None:
        raise ValueError("Cannot find model in XML at path ./diagram/mxGraphModel/root")

    element = model.find('object[@label="<div>{}</div>"]'.format(settings['root_package']))
    if element is None:
        raise ValueError("Root packaged element not found. Settings has:{}".format(settings['root_package']))

    model_package: UMLPackage = package_parse(element, root, None)

    return model_package, test_cases


def package_parse(element, root_element, parent_package: Optional[UMLPackage]) -> UMLPackage:
    """ Extract package details, call class parser for classes and self parser for sub-packages.
    Association linking is not done here, but in a 2nd pass using the parse_associations function.
    """
    name = element.get("label").split("div>")[1].split("</")[0]
    id = element.get('id')

    package = UMLPackage(id, name, parent_package)

    model = root_element.find('./diagram/mxGraphModel/root')
    child_elements = model.findall('object/mxCell[@parent="{}"]'.format(id))

    # Parse classes
    for element in child_elements:
        object_element = element.find("..")
        element_type = object_element.get("UMLType")

        if element_type == "Class":
            cls = class_parse(package, object_element, root_element)
            package.classes.append(cls)

    # Classes are needed to parse generalisations and associations
    for element in child_elements:
        object_element = element.find("..")
        element_type = object_element.get("UMLType")

        if element_type == "Generalization":
            generalization_parse(package, object_element, root_element)
        elif element_type == "Association":
            association_parse(package, object_element, root_element)

    return package


def generalization_parse(package: UMLPackage, element, root):
    cell = element.find("mxCell")
    source: UMLClass = package.find_by_id(cell.get("source"))
    target: UMLClass = package.find_by_id(cell.get("target"))
    source.supertype = target


def association_parse(package: UMLPackage, element, root):
    cell = element.find("mxCell")
    source: UMLClass = package.find_by_id(cell.get("source"))
    target: UMLClass = package.find_by_id(cell.get("target"))

    UMLAssociation(package, source, target)


def class_parse(package: UMLPackage, element, root) -> UMLClass:
    label = element.get("label").split(",")[-1].split("div>")
    if len(label) == 1:
        name = label[0].strip("<b>").strip("</b>").strip("i>").strip("</i")
    else:
        name = label[-2].strip("<b>").strip("</b></").strip("i>").strip("</i")

    id = element.get("id")
    cls = UMLClass(package, name, id)

    abstract = element.get("Abstract")
    if abstract is not None and abstract == "True":
        cls.is_abstract = True

    children = root.findall('./diagram/mxGraphModel/root/mxCell[@parent="{}"]'.format(id))
    # Grab a list of the attribute stereotypes and their heights
    stereotypes = []
    for child in children:
        value = child.get("value")
        if "<<" in value:
            geometry = child.find("mxGeometry")
            stereotypes.append((value.strip("<<").strip(">>"), int(geometry.get("y"))))

    # Create all the attributes
    for child in children:
        value = child.get("value")
        if value[0:2] != "<<":
            attr = attr_parse(cls, child, root, stereotypes)
            cls.attributes.append(attr)

    return cls


def attr_parse(parent: UMLClass, element, root, stereotypes):
    value = element.get("value").strip("<div>").strip("</div>").strip("<br")
    # height = int(element.find("mxGeometry").get("y"))

    is_id = False
    if "{id}" in value:
        is_id = True
        value = value.strip("{id}").strip()

    visibility: bool = False
    if value.startswith("+"):
        visibility = True
    value = value.strip("+").strip("-").strip()

    name, attr_type = value.split(":")
    attr_type = attr_type.strip()

    attr = UMLAttribute(parent, name, element.get('id'))
    if is_id:
        attr.is_id = is_id
        parent.id_attribute = attr
    attr.visibility = visibility

    attr.type = attr_type
    if attr.type == 'string':
        attr.length = 100

    if attr_type in generation_fields[settings['generation_type']].keys():
        attr.dest_type = generation_fields[settings['generation_type']][attr_type]
    else:
        attr.dest_type = attr_type

    # print("{} | {} | {} | {}".format(name, attr_type, is_id, height))

    return attr