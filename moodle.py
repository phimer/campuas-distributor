from selenium import webdriver

#  from webdriver_manager.chrome import ChromeDriverManager
import login_info
import kurs_info
from termcolor import colored
from time import sleep
from pynput.mouse import Button, Controller
import db


# original_kennungen_table_name = "OriginalKennungen"
# verteilte_kennungen_table_name = "VerteilteKennungen"
# login_seite = "https://moodle.frankfurt-university.de/login/index.php"
# kurs_link = "https://campuas.frankfurt-university.de/course/view.php?id=4239"


class MoodleBot:
    def __init__(self):
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())

        # set kurs link here
        self.kurs_link = kurs_info.kurs_link
        self.login_seite = kurs_info.login_seite
        self.original_kennungen_table_name = kurs_info.original_kennungen_table_name
        self.verteilte_kennungen_table_name = kurs_info.verteilte_kennungen_table_name
        self.login = login_info.login
        self.password = login_info.password

    def db_result_to_string(self, login_password):
        login = login_password[0]
        password = login_password[1]

        return f"Login: {login} Password: {password}"

    def check_if_data_already_in_table(self):
        count = int(db.get_count_of_rows(table=self.original_kennungen_table_name))

        if count > 0:
            return True, count

        return False, 0

    def save_csv_in_database(self, csv_file_path):
        x = db.insert_csv(
            csv_file_path=csv_file_path, table_name=self.original_kennungen_table_name
        )

        print("CSV imported.")

    def start(self):
        self.driver = webdriver.Firefox()
        self.mouse = Controller()

        # auf login navigieren
        self.driver.get(self.login_seite)

        sleep(2)

        self.driver.find_element(
            by="xpath",
            value="/html/body/div[2]/div[3]/section/aside/section[2]/div/div/div/div[2]/div/div/a",
        ).click()
        sleep(2)

        login = self.driver.find_element(by="id", value="username")
        login.send_keys(self.login)

        password = self.driver.find_element(by="id", value="password")
        password.send_keys(self.password)

        # login button
        self.driver.find_element(by="name", value="_eventId_proceed").click()
        print("clicked login button")

        sleep(2)

        # navigate to course
        # self.driver.get(self.kurs_link)
        # print("navigated to course")

        # sleep(2)

        # navigate to abgabe
        # self.driver.find_element(
        #     by="xpath",
        #     value="/html/body/div[3]/div[4]/div[2]/div[3]/div/section/div/div/div/ul/li[1]/div[2]/ul/li[2]/div/div[1]/div/div[1]/div/div[2]/div[2]/a",
        # ).click()
        # print("navigated to abgabe")

        # navigate directly to abgabe
        self.driver.get(
            "https://campuas.frankfurt-university.de/mod/assign/view.php?id=215998"
        )

        # click Grade
        self.driver.find_element(
            by="xpath",
            value="/html/body/div[2]/div[4]/div[2]/div[3]/div/section/div[2]/div[1]/div/div[2]/a",
        ).click()

        print("sleep 10 before verteilung")
        sleep(10)

        ########### verteilung beginnt ################
        abgabe_check = False  # checkt ob Student eigene Abgabe gemacht hat
        i = 0
        for i in range(100):
            print("sleep 20")
            # check jedes mal auf false setzen - wird benutzt um zu sehen ob student (RICHTIGE) abgabe gemacht hat - nur wenn wird weiter gemacht, sonst student übersprungen
            abgabe_check = False

            print(f"\n{i+1}")

            # get student info
            raw_student_info = self.driver.find_element(by="tag name", value="h4").text

            student_info_split = raw_student_info.splitlines()

            student_name = student_info_split[0]

            student_email = student_info_split[1]

            print(student_name)
            print(student_email)

            # check ob student schon kennung hat - checkt nur ob das feld leer ist oder nicht, nicht was er bekommen hat
            # else case verteilt Kennung an student
            antwort_feld_text = self.driver.find_element(
                by="id",
                value="id_assignfeedbackcomments_editoreditable",
            ).text

            if antwort_feld_text != "":
                print(
                    colored(
                        f"Student {student_name} hat schon Kennung bekommen", "magenta"
                    )
                )

            else:
                print(colored(f"{student_name} - {student_email}", "white"))

                # student abgabe - hoffentlich matrikelnummer
                try:
                    student_abgabe = self.driver.find_element(
                        by="class name", value="no-overflow"
                    ).text
                    print(f"Student Abgabe: {student_abgabe}")

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
                # if - nur wenn student abgabe gemacht hat, bekommt er auch VM
                if abgabe_check:
                    # in editor feld clicken
                    self.driver.find_element(
                        by="class name", value="editor_atto_content"
                    ).click()

                    # login und pw aus database holen
                    result = db.get_first_entry(self.original_kennungen_table_name)
                    result_id = result[0]
                    result_kennung = result[1]
                    result_password = result[2]

                    # kennung und student info in neue table schreiben
                    db.insert(
                        self.verteilte_kennungen_table_name,
                        result_kennung,
                        result_password,
                        student_name,
                        student_email,
                        student_abgabe,
                    )
                    print(colored("neue Daten in Datenbank geschrieben", "green"))

                    # login und pw aus db löschen
                    db.delete(table=self.original_kennungen_table_name, id=result_id)
                    print(colored("login und pw aus table gelöscht", "green"))

                    # text in feld eingeben
                    login_pw_string = result[1] + " - " + result[2]

                    self.driver.find_element(
                        by="xpath",
                        value='//*[@id="id_assignfeedbackcomments_editoreditable"]',
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
            nextbutton = self.driver.find_element(by="name", value="saveandshownext")
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
