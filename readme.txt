Simple Script using Selenium and Geckodriver/Chromedriver to distribute Login Information to Students via CampUAS.

Installation Guide:

conda create -n moodle python=3.10
conda activate moodle

pip install -r requirements.txt

install latest version of geckodriver: https://github.com/mozilla/geckodriver/releases

create python file: login_info.py
save login and password in varibales 'login' and 'password' as strings

add/adjust info in kurs_info.py

Start with: python main.py
