from typing import List, Dict
from defs.table_def import TableDef
from defs.column_def import ColumnDef
from defs.relation_def import RelationshipDef, RelationshipType
from jinja2 import FileSystemLoader, Environment


def generate_create_table_statement(table_def: TableDef) -> str:
    """
    Create a table in the database based on the table def
    :param table_def: Definition provided by the user
    :return: Create table statement
    """

    column_defs = table_def.columnDefs

    # load jinja template from file templates/create_table.jinja2
    env = Environment(loader=FileSystemLoader("parsers/templates"))
    template = env.get_template("create_table.jinja2")
    # render the template with the table definition
    statement = template.render(
        table_name=table_def.name,
        parent_table=table_def.parent_table,
        columnDefs=column_defs,
    )

    return statement


def _generate_index_create_statement(column_def: ColumnDef, table_name: str) -> str:
    """
    Generate an index name based on the table and column name
    :return:
    """
    env = Environment(loader=FileSystemLoader("pgmeta/parsers/templates"))

    template = env.get_template("create_index.jinja2")
    statement = template.render(
        index_name=column_def.index_name,
        table_name=table_name,
        index_type=column_def.index_type,
        column_name=column_def.name,
    )

    return statement


def generate_create_index_statement(table_def: TableDef) -> List[str]:
    """
    Create an index on a column in the table
    :param table_def: Table definition
    :param column_name: Column name
    :return: Create index statement
    """
    statements = []
    # if there is no column have index: True, return None
    for column_def in table_def.columnDefs:
        if (
            column_def.index
            and not column_def.is_primary_key
            and not column_def.is_unique
            and not column_def.is_vector_index
        ):
            stmt = _generate_index_create_statement(column_def, table_def.name)
            statements.append(stmt)

    return statements


def generate_m2m_relation_statement(relation_def: RelationshipDef) -> str:
    """
    Generate a many-to-many relation statement.
    :param relation_def: Relationship definition
    :param schema: Dictionary of table definitions
    :return: SQL statement for creating the many-to-many relation
    """
    if relation_def.relationship_type != RelationshipType.MANY_TO_MANY:
        raise ValueError("This function only handles MANY_TO_MANY relationships")

    junction_table_name = f"{relation_def.from_table}_{relation_def.to_table}"

    env = Environment(loader=FileSystemLoader("parsers/templates"))
    template = env.get_template("create_m2m_reln.jinja2")
    statement = template.render(
        table_name=junction_table_name,
        from_table=relation_def.from_table,
        from_ref_column=relation_def.from_column,
        to_table=relation_def.to_table,
        to_ref_column=relation_def.to_column,
    )

    return statement


def generate_foreign_key_statement(relation_def: RelationshipDef) -> str:
    """
    Generate a foreign key statement for ONE_TO_MANY, MANY_TO_ONE, and ONE_TO_ONE relationships.
    :param relation_def: Relationship definition
    :return: SQL statement for creating the foreign key
    """
    if relation_def.relationship_type == RelationshipType.MANY_TO_MANY:
        raise ValueError("This function does not handle MANY_TO_MANY relationships")

    constraint_name = f"fk_{relation_def.from_table}_{relation_def.from_column}_to_{relation_def.to_table}_{relation_def.to_column}"

    env = Environment(loader=FileSystemLoader("parsers/templates"))
    template = env.get_template("create_foreign_key.jinja2")
    statement = template.render(
        table_name=relation_def.from_table,
        constraint_name=constraint_name,
        column_name=relation_def.from_column,
        fk_table=relation_def.to_table,
        fk_column=relation_def.to_column,
    )

    return statement


def generate_relation_statement(relation_def: RelationshipDef) -> str:
    """
    Generate the appropriate relation statement based on the relationship type.
    :param relation_def: Relationship definition
    :param schema: Dictionary of table definitions
    :return: SQL statement for creating the relation
    """
    if relation_def.relationship_type == RelationshipType.MANY_TO_MANY:
        return generate_m2m_relation_statement(relation_def)
    else:
        return generate_foreign_key_statement(relation_def)
