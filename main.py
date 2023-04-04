import db
from moodle import MoodleBot

bot = MoodleBot()


user_input = input("do you want to import a csv file into the database? (y/n)\n")


if user_input == "y":

    file_path = "OOP_WS20-21_Accounts.csv"

    check, count = bot.check_if_data_already_in_table()

    if check:
        print(
            f"There are already {count} Entries form another csv file in the database."
        )
        user_input = input(
            "Are you sure that an additional file should be imported?. (y/n)\n"
        )

        if user_input == "y":
            bot.save_csv_in_database(file_path)
    else:
        bot.save_csv_in_database(file_path)


user_input = input("Do you want to start the bot? (y/n)\n")

if user_input == "y":
    bot.start()
else:
    # exit
    pass
