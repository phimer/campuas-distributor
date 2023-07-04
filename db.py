import sqlite3
from csv import writer, reader


con = sqlite3.connect("data.db")
c = con.cursor()


def get_first_entry(table):

    c.execute(f"""SELECT * from {table} LIMIT 1;""")
    login_password = c.fetchone()

    return login_password


def delete(table, id):

    c.execute(f"""DELETE from {table} WHERE id=?""", [id])

    con.commit()


def insert(
    table,
    moodle_kennung,
    moodle_pw,
    moodle_student_name,
    moodle_student_emal,
    moodle_matrikel_nummer,
):

    c.execute(
        f"INSERT INTO {table} (kennung, password, name, email, matrikelnr) VALUES(?,?,?,?,?)",
        (
            moodle_kennung,
            moodle_pw,
            moodle_student_name,
            moodle_student_emal,
            moodle_matrikel_nummer,
        ),
    )

    con.commit()


def insert_csv(csv_file_path, table_name):

    con.execute(
        f"create table if not exists {table_name} (id integer primary key autoincrement, kennung varchar(60) NOT NULL, password varchar(60) NOT NULL)"
    )

    csv_list = []

    with open(csv_file_path, "r") as file:
        csv_reader = reader(file, delimiter=";")
        for row in csv_reader:
            kennung = row[0]
            password = row[3]
            csv_list.append((kennung, password))

    con.executemany(
        f"INSERT INTO {table_name}(kennung, password) values (?,?)", csv_list
    )
    con.commit()


def get_count_of_rows(table):

    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';"
    result = con.execute(query)
    if result.fetchone() is None:
        return 0
    else:
        return c.execute(f"SELECT count(*) FROM {table}").fetchall()[0][0]


def create_table_verteilte_kennungen():
    create_table_query = """
        CREATE TABLE VerteilteKennungen (
            KENNUNG TEXT PRIMARY KEY,
            PASSWORD TEXT NOT NULL,
            NAME TEXT NOT NULL,
            EMAIL TEXT NOT NULL,
            MATRIKELNR TEXT
        );
    """

    con.execute(create_table_query)
    con.commit()
    print("Created table VerteilteKennungen")


def create_table_original_kennungen():
    create_table_query = """
        CREATE TABLE OriginalKennungen (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            KENNUNG TEXT NOT NULL,
            PASSWORD TEXT NOT NULL
        );
    """

    con.execute(create_table_query)
    con.commit()
    print("Created table VerteilteKennungen")


# result = con.execute(query)
# x = result.fetchone()
# print(x)
# original_kennungen_table_name = "OriginalKennungen"
# verteilte_kennungen_table_name = "VerteilteKennungen"
# result = get_first_entry(original_kennungen_table_name)

# print(result[0])

# delete(original_kennungen_table_name, result[0])

# con.commit()
