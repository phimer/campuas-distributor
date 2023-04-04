from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from login_info import login, password
from termcolor import colored
import sys
from time import sleep
from pynput.mouse import Button, Controller
import sqlite3
import db

log = login
pw = password

ibis = "https://moodle.frankfurt-university.de/mod/assign/view.php?id=325540&action=grader%2F&userid=7793"
ebis = "https://moodle.frankfurt-university.de/mod/assign/view.php?id=352969&action=grader%2F&userid=58746"


inp = input("ibis oder ebis\n")


class MoodleBot:
    def __init__(self):
        # self.driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

        self.mouse = Controller()

    def db_result_to_string(self, login_password):

        login = login_password[0]
        password = login_password[1]

        return f"Login: {login} Password: {password}"

    def main(self, table, kurs, kurs_table):

        self.driver.get("https://moodle.frankfurt-university.de/login/index.php")

        login = self.driver.find_element_by_xpath('//*[@id="username"]')
        login.send_keys(log)

        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys(pw)

        # login button
        self.driver.find_element_by_xpath('//*[@id="loginbtn"]').click()

        print("clicked login button")

        # kurs aus function argument
        self.driver.get(kurs)

        sleep(5)

        print(colored("sleep 10", "green"))
        sleep(10)

        # self.driver.find_element_by_name('sendstudentnotifications').click()

        # just for demo
        # for i in range(50):
        #     sleep(1)
        #     print(i)

        # sleep(5)

        ########### verteilung beginnt ################
        abgabe_check = False  # checkt ob Student eigene Abgabe gemacht hat
        i = 0
        while True:  # muss man noch hoch setzen - wie hoch? --egal weil check if bla

            print("sleep 20 click that")
            # check jedes mal auf false setzen - wird benutzt um zu sehen ob student (RICHTIGE) abgabe gemacht hat - nur wenn wird weiter gemacht, sonst student übersprungen
            abgabe_check = False

            print(f"\n{i+1}")
            # print(f'\n{i+1}')

            # get student info
            raw_student_info = self.driver.find_element_by_tag_name("h4").text

            studen_info_split = raw_student_info.splitlines()

            student_name = studen_info_split[0]

            student_email = studen_info_split[1]

            # check ob student schon kennung hat - checkt nur ob das feld leer ist oder nicht, nicht was er bekommen hat
            # else case gibt student kennung
            antwort_feld_text = self.driver.find_element_by_xpath(
                "/html/body/div[5]/div/div/div[3]/div/div[2]/form/fieldset[1]/div/div[3]/div[2]/div[1]/div[1]/div/div[2]/div"
            ).text

            if antwort_feld_text != "":
                print(
                    colored(
                        f"Student {student_name} hat schon Kennung bekommen", "magenta"
                    )
                )

            else:

                # letzte Zeile von 3 Zeiligem Strimg entfernen

                print(colored(f"{student_name} - {student_email}", "white"))

                # student abgabe - hoffentlich matrikelnummer
                try:
                    student_abgabe = self.driver.find_element_by_class_name(
                        "no-overflow"
                    ).text

                    if str(student_abgabe).isdigit() and len(str(student_abgabe)) == 7:

                        print(
                            colored(
                                f"Matrikelnummer angegeben\n{student_abgabe}", "yellow"
                            )
                        )
                        abgabe_check = True

                    elif (
                        str(student_abgabe).isdigit() and len(str(student_abgabe)) == 6
                    ):

                        print(
                            colored(
                                f"Matrikelnummer angegeben\n{student_abgabe}", "yellow"
                            )
                        )
                        abgabe_check = True
                    else:
                        print(
                            colored(
                                f"Student hat keine Matrikelnummer eingegeben\n{student_abgabe}",
                                "orange",
                            )
                        )

                except:
                    print(colored("Student ohne Abgabe", "red"))
                # if - nur wenn student abgage gemacht hat, bekommt er auch VM
                if abgabe_check:
                    # in editor feld clicken
                    print(colored("in feld clicken", "blue"))
                    self.driver.find_element_by_xpath(
                        '//*[@id="id_assignfeedbackcomments_editoreditable"]'
                    ).click()
                    # login und pw aus database holen
                    login_pw_string = self.db_result_to_string(
                        db.get_first_entry(table)
                    )
                    # kennung und studen info in neue table schreiben
                    # [0] ist, weil .read_one_line_from_table ein sqlite object/liste returned
                    db.insert(
                        kurs_table,
                        db.get_first_entry(table)[0],
                        db.get_first_entry(table)[1],
                        student_name,
                        student_email,
                        student_abgabe,
                    )
                    print(colored("neue Daten in Datenbank geschrieben", "green"))
                    # login und pw aus db löschen
                    db.delete_first_item_from_table(table, db.get_first_entry(table)[0])
                    print(colored("login und pw aus table gelöscht", "green"))
                    # text in feld eingeben
                    print(colored("VM Kennung vergeben", "blue"))
                    self.driver.find_element_by_xpath(
                        '//*[@id="id_assignfeedbackcomments_editoreditable"]'
                    ).send_keys(login_pw_string)
                    print(
                        colored(
                            f"{login_pw_string} vergeben an:\n{student_name} - {student_email}\n{student_abgabe}",
                            "white",
                            "on_red",
                        )
                    )
            sleep(1)
            # die nächsten 2 Schritte müssen bei jeder loop ausgeführt werden, da sie zum nächsten studenten springen
            # click save and next
            print(colored("click save and show next", "white"))
            nextbutton = self.driver.find_element_by_name("saveandshownext")
            nextbutton.click()
            # click ok button
            print(colored("3 sec sleep - click ok", "white"))
            sleep(3)
            self.mouse.position = (434, 434)
            self.mouse.click(Button.left, 1)

            sleepy = 10
            print(colored(f"{sleepy} sec sleep", "white"))
            sleep(sleepy)  # maybe higher?

            i = i + 1
        print(colored("ENDE", "red"))

        ########################################################################################################################################################################################
        # absenden
        # self.driver.find_element_by_xpath('//*[@id="yui_3_17_2_1_1597766494186_623"]').click()
        # self.driver.find_element_by_xpath('//*[@id="yui_3_17_2_1_1597766494186_1337"]').click()
        # self.driver.find_element_by_xpath('//*[@id="module-288410"]/div/div/div[2]/div/a/span').click()
        # self.driver.find_element_by_xpath('//*[@id="module-288410"]/div/div/div[2]/div/a/span').click()
        # self.driver.find_element_by_xpath('//*[@id="module-288410"]/div/div/div[2]/div/a/span').click()
        # self.driver.find_element_by_xpath('//*[@id="module-288410"]/div/div/div[2]/div/a/span').click()
        # self.driver.find_element_by_xpath('//*[@id="module-288410"]/div/div/div[2]/div/a/span').click()


moodle_bot = MoodleBot()
# bot.main('oop_vm_ibis', ibis, 'oop_vm')
# bot.main('oop_vm_ebis', ebis, 'oop_vm_final_ebis')


if inp == "ibis":
    moodle_bot.main("oop_vm_ibis", ibis, "oop_vm")
    print(colored("IBIS", "green"))
elif inp == "ebis":
    moodle_bot.main("oop_vm_ebis", ebis, "oop_vm_final_ebis")
    print(colored("EBIS", "green"))
else:
    print(colored("falscher input", "red"))


#     def main(self, table, kurs, kurs_table):
