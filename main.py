import db
from moodle import MoodleBot

bot = MoodleBot()

try:
    db.create_table_verteilte_kennungen()
    print("Created Table VerteilteKennungen")
except:
    print("Table VerteilteKennungen exists")

try:
    db.create_table_original_kennungen()
    print("Created Table OriginalKennungen")
except:
    print("Table OriginalKennungen exists")


user_input = input("Do you want to import a csv file into the database? (y/n)\n")

if user_input == "y":

    file_path = input("Enter filepath for csv:\n")

    check, count = bot.check_if_data_already_in_table()

    if check:
        print(
            f"There are already {count} Entries form another csv file in the database."
        )
        user_input = input(
            "Are you sure that an additional file should be imported?. (y/n)\n"
        )

        if user_input == "y":
            try:
                bot.save_csv_in_database(file_path)
            except:
                print("Error while importing csv file - start program again.")
                exit()
    else:
        bot.save_csv_in_database(file_path)


user_input = input("Do you want to start the bot? (y/n)\n")

if user_input == "y":
    bot.start()
else:
    # exit
    pass
