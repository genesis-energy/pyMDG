# Default is JSON Schema Specification
generation_fields = {
    "default": {
        "bool": "boolean",
        "Date": "date",
        "dateTime": "date-time",
        "decimal": "number",
        "Decimal": "number",
        "enum": "enum",
        "int": "integer",
        "bigint": "integer",
        "Integer": "integer",
        "long": "integer",
        "String": "string",
        "str": "string",
    },
    "avro": {
        "bool": "boolean",
        "Date": "date",
        "dateTime": "date-time",
        "decimal": "number",
        "Decimal": "number",
        "enum": "enum",
        "int": "int",
        "integer": "int",
        "bigint": "int",
        "Integer": "int",
        "long": "int",
        "String": "string",
        "str": "string",
    },
    "spring data rest": {
        "boolean": "boolean",
        "date": "Date",
        "dateTime": "DateTime",
        "decimal": "Double",
        "enum": "String",
        "int": "int",
        "bigint": "int",
        "integer": "int",
        "long": "int",
        "string": "String",
    },
    "django": {
        "boolean": "BooleanField",
        "int": "IntegerField",
        "bigint": "BigIntegerField",
        "decimal": "DecimalField",
        "string": "CharField",
        "str": "CharField",
        "String": "CharField",
        "text": "TextField",
        "duration": "DurationField",
        "file": "FileField",
        "float": "FloatField",
        "date": "DateField",
        "dateTime": "DateTimeField",
        "datetime": "DateTimeField",
        "date_time": "DateTimeField",
        "Timestamp": "DateTimeField",
        "timestamp": "DateTimeField",
        "json": "JSONField",
    },
    "marshmallow": {
        "boolean": "Boolean",
        "int": "Integer",
        "integer": "Integer",
        "bigint": "Integer",
        "decimal": "Decimal",
        "string": "String",
        "text": "Text",
        "duration": "Duration",
        "file": "File",
        "float": "Float",
        "date": "Date",
        "dateTime": "DateTime",
        "date_time": "DateTime",
    },
    "sqlalchemy": {
        "boolean": "Boolean",
        "int": "Integer",
        "integer": "Integer",
        "string": "String",
        "decimal": "Numeric",
        "Decimal": "Numeric",
        "float": "Float",
        "date": "Date",
        "dateTime": "DateTime",
        "date_time": "DateTime",
    },
    "python": {
        "Integer": "int",
        "String": "str",
        "string": "str",
        "Float": "float",
        "Numeric": "Decimal",
        "Boolean": "bool",
        "DECIMAL": "Decimal",
        "CHAR": "str",
        "TIMESTAMP": "datetime.timestamp",
        "DATE": "date",
        "INTEGER": "int",
        "VARCHAR": "str",
    },
    "ddl": {
        "Integer": "NUMBER",
        "int": "NUMBER",
        "String": "VARCHAR2",
        "string": "VARCHAR2",
        "str": "VARCHAR2",
        "decimal": "NUMBER",
    },
}
