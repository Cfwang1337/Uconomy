import os
import numpy as np
import pandas as pd


def main():

    source_dir = os.path.expanduser("~/gh/Uconomy/to_load_to_sql")
    destination_dir = os.path.expanduser("~/gh/Uconomy/sql_to_db")

    destination_dir_files = list(os.listdir(destination_dir))

    for filename in os.listdir(source_dir):
        print filename
        if "{0}.tsv".format(filename) not in destination_dir_files:

            table_name = filename.split('.')[0]

            if filename[-3:] == "csv":
                file_df = pd.DataFrame.from_csv(os.path.join(source_dir, filename), index_col=None)
            elif filename[-3:] in ["txt", "tab"]:
                file_df = pd.read_csv(os.path.join(source_dir, filename), sep='\t', index_col=None)

            file_df = file_df.replace(np.nan, "\N", regex=True)

            try:
                file_df.to_csv(os.path.join(destination_dir, "{0}.tsv".format(filename)), sep='|', index=None, header=None,
                               encoding="utf-8")
            except:
                file_df = file_df.replace(r'[^\x00-\x7F]+', " ", regex=True)
                file_df.to_csv(os.path.join(destination_dir, "{0}.tsv".format(filename)), sep='|', index=None, header=None,
                           encoding="utf-8")

            column_list = []

            for df_column in file_df.columns:
                # print file_df[df_column]
                if file_df[df_column].dtype == "object":

                    field_length = file_df[df_column].astype(str).map(len)
                    column_type = "VARCHAR({0})".format(max(field_length))

                elif file_df[df_column].dtype == "float64":
                    column_type = "FLOAT8"
                elif file_df[df_column].dtype == "int64":
                    column_type = "INT8"

                column_string = "{0} {1},".format(df_column, column_type)
                column_list.append(column_string)

            column_string = "\n".join(column_list)[:-1]

            SQL_text = """CREATE TABLE {0}
            (
                {1}
            );
            COPY {0} FROM '{2}' (FORMAT TEXT, DELIMITER '|');
            """.format(table_name, column_string, os.path.join(destination_dir, "{0}.tsv".format(filename)))

            print SQL_text

            with open(os.path.join("sql_to_db", "{0}.sql".format(filename)), 'wb') as writefile:
                writefile.write(SQL_text)

        else:
            print "ALREADY PROCESSED"

    return

if __name__ == "__main__":
    main()