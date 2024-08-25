import argparse
import os
from generate import read_definitions, generate_sql_statements

def main():
    parser = argparse.ArgumentParser(description="Generate SQL statements from JSON definitions.")
    parser.add_argument("directory", help="Path to the directory containing JSON definition files")
    parser.add_argument("-o", "--output", help="Output directory for SQL files", default=".")
    args = parser.parse_args()

    all_defs = read_definitions(args.directory)

    statements = generate_sql_statements(all_defs)
    
    os.makedirs(args.output, exist_ok=True)

    for i, defs in enumerate(all_defs):
        output_file = os.path.join(args.output, f"{os.path.splitext(os.path.basename(defs.tableDefs[0].name))[0]}.sql")
        with open(output_file, "w") as f:
            f.write("\n".join(statements[i]))
        print(f"SQL statements written to {output_file}")

if __name__ == "__main__":
    main()
