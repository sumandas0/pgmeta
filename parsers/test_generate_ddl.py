from parsers.generate_ddl import TableDef, generate_create_table_statement, ColumnDef
from defs.relation_def import RelationshipDef, RelationshipType
from parsers.generate_ddl import generate_relation_statement

base_table = {
    "name": "Base",
    "columnDefs": [
        {
            "name": "uuid",
            "data_type": "VARCHAR(36)",
            "is_nullable": False,
            "is_unique": True,
            "is_primary_key": True,
            "index": True,
            "index_name": "uuid_index",
            "index_type": "BTREE",
        },
        {
            "name": "type_name",
            "data_type": "TEXT",
            "is_nullable": False,
            "is_unique": False,
            "is_primary_key": False,
            "index": True,
            "index_name": "type_name_index",
            "index_type": "BTREE",
        },
        {
            "name": "qualified_name",
            "data_type": "TEXT",
            "is_nullable": False,
            "is_unique": False,
            "is_primary_key": False,
            "index": True,
            "index_name": "qualified_name_index",
            "index_type": "BTREE",
        },
        {
            "name": "created_at",
            "data_type": "TIMESTAMP",
            "is_nullable": False,
            "is_unique": False,
            "is_primary_key": False,
            "index": True,
            "index_name": "created_at_index",
            "index_type": "BTREE",
        },
        {
            "name": "updated_at",
            "data_type": "TIMESTAMP",
            "is_nullable": False,
            "is_unique": False,
            "is_primary_key": False,
            "index": True,
            "index_name": "updated_at_index",
            "index_type": "BTREE",
        },
        {
            "name": "created_by",
            "data_type": "VARCHAR(36)",
            "is_nullable": False,
            "is_unique": False,
            "is_primary_key": False,
            "index": True,
            "index_name": "created_by_index",
            "index_type": "BTREE",
        },
        {
            "name": "updated_by",
            "data_type": "VARCHAR(36)",
            "is_nullable": False,
            "is_unique": False,
            "is_primary_key": False,
            "index": True,
            "index_name": "updated_by_index",
            "index_type": "BTREE",
        },
    ],
}
table_example_1 = {
    "name": "Repository",
    "parent_table": "Base",
    "columnDefs": [
        {
            "name": "repository_name",
            "data_type": "TEXT",
            "is_nullable": False,
            "is_primary_key": False,
            "is_unique": True,
            "index": True,
            "index_name": "repository_name_index",
            "index_type": "BTREE",
        },
        {
            "name": "provider",
            "data_type": "VARCHAR(36)",
            "is_nullable": True,
            "is_primary_key": False,
            "is_unique": False,
            "index": False,
            "index_name": "provider_index",
            "index_type": "BTREE",
        },
    ],
}

# Load the table definition as a TableDef object


def test_load_definition():
    base_table_def = TableDef(**base_table)
    assert base_table_def.name == "Base"
    assert len(base_table_def.columnDefs) == 7
    assert base_table_def.columnDefs[0].name == "uuid"
    assert base_table_def.columnDefs[0].data_type == "VARCHAR(36)"
    assert base_table_def.columnDefs[0].is_nullable is False
    assert base_table_def.columnDefs[0].is_unique is True
    assert base_table_def.columnDefs[0].is_primary_key is True
    assert base_table_def.columnDefs[0].index is True
    assert base_table_def.columnDefs[0].index_name == "uuid_index"
    assert base_table_def.columnDefs[0].index_type == "BTREE"


def test_create_base_table():
    base_table_def = TableDef(**base_table)
    statement = generate_create_table_statement(base_table_def)
    assert (
        statement
        == """CREATE TABLE IF NOT EXISTS Base
(

        uuid VARCHAR(36) NOT NULL UNIQUE PRIMARY KEY,

        type_name TEXT NOT NULL,

        qualified_name TEXT NOT NULL,

        created_at TIMESTAMP NOT NULL,

        updated_at TIMESTAMP NOT NULL,

        created_by VARCHAR(36) NOT NULL,

        updated_by VARCHAR(36) NOT NULL

)
"""
    )


def test_create_table_example_1():
    table_def = TableDef(**table_example_1)
    statement = generate_create_table_statement(table_def)
    assert (
        statement
        == """CREATE TABLE IF NOT EXISTS Repository
(

        repository_name TEXT NOT NULL UNIQUE,

        provider VARCHAR(36)

)
INHERITS (Base)"""
    )


def test_generate_relation_statement_one_to_many():
    relation_def = RelationshipDef(
        name="Post",
        relationship_type=RelationshipType.ONE_TO_MANY,
        from_table="Post",
        from_column="user_id",
        to_table="User",
        to_column="id",
    )
    statement = generate_relation_statement(relation_def)
    assert trim_statement(statement) == trim_statement(
        """ALTER TABLE Post
ADD CONSTRAINT fk_Post_user_id_to_User_id
FOREIGN KEY (user_id)
REFERENCES User (id)"""
    )


def test_generate_relation_statement_many_to_many():
    relation_def = RelationshipDef(
        name="Course_Student",
        relationship_type=RelationshipType.MANY_TO_MANY,
        from_table="Course",
        from_column="id",
        to_table="Student",
        to_column="id",
    )
    statement = generate_relation_statement(relation_def)
    assert trim_statement(statement) == trim_statement(
        """
        CREATE TABLE IF NOT EXISTS Course_Student (
            Course_id VARCHAR(36) REFERENCES Course(id) NOT NULL,
            Student_id VARCHAR(36) REFERENCES Student(id) NOT NULL,
            PRIMARY KEY (Course_id, Student_id)
        )
        CREATE INDEX IF NOT EXISTS idx_Course_Student_Course_id ON Course_Student(Course_id);
        CREATE INDEX IF NOT EXISTS idx_Course_Student_Student_id ON Course_Student(Student_id);
        """
    )


def test_generate_relation_statement_one_to_one():
    relation_def = RelationshipDef(
        name="Passport",
        relationship_type=RelationshipType.ONE_TO_ONE,
        from_table="Passport",
        from_column="person_id",
        to_table="Person",
        to_column="id",
    )
    statement = generate_relation_statement(relation_def)
    assert trim_statement(statement) == trim_statement(
        """ALTER TABLE Passport
ADD CONSTRAINT fk_Passport_person_id_to_Person_id
FOREIGN KEY (person_id)
REFERENCES Person (id)"""
    )


# Function to trim all the spaces, newlines, and tabs from generated statements to make them easier to compare
def trim_whitespace(statement: str) -> str:
    return "".join(statement.split())


def trim_newlines_and_tabs(statement: str) -> str:
    return statement.replace("\n", "").replace("\t", "")


def trim_statement(statement: str) -> str:
    return trim_whitespace(trim_newlines_and_tabs(statement))
