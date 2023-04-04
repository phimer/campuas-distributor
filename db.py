import sqlite3
from csv import writer, reader


connection = sqlite3.connect("data.db")
c = connection.cursor()


def get_first_entry(table):

    c.execute(f"""SELECT * from {table} LIMIT 1;""")
    login_password = c.fetchone()

    return login_password


def delete_first_item_from_table(table, id):

    c.execute(f"""DELETE from {table} WHERE id=?""", [id])

    connection.commit()


def insert(
    table,
    moodle_id,
    moodle_pw,
    moodle_student_name,
    moodle_student_emal,
    moodle_matrikel_nummer,
):

    c.execute(
        f"INSERT INTO {table} (id, password, student_name, student_email, matrikel_nummer) VALUES(?,?,?,?,?)",
        (
            moodle_id,
            moodle_pw,
            moodle_student_name,
            moodle_student_emal,
            moodle_matrikel_nummer,
        ),
    )

    connection.commit()


# print(read_one_db())

# delete_first_item_from_db(read_one_db()[0])

# print(read_one_db()[0])


# con.commit()
