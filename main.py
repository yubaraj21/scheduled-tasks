from datetime import datetime
import pandas
import random
import smtplib
import os

MY_EMAIL = os.environ.get("yubarajbauri13@gmail.com")
MY_PASSWORD = os.environ.get("keglehyihbwgmcav")

if not MY_EMAIL or not MY_PASSWORD:
    raise ValueError("Email credentials are not set in the environment variables.")

today = datetime.now()
today_tuple = (today.month,today.day)

try:
    data = pandas.read_csv("birthdays.csv")
except FileNotFoundError:
    raise FileNotFoundError("The birthdays.csv file was not found.")
birthdays_dict = {(data_row["month"],data_row["day"]): data_row for (index, data_row) in data.iterrows()}
if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
    try:
        with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("NAME", birthday_person["name"])
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file {file_path} not found.")
        
    try:
        with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL,MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,to_addrs=birthday_person["email"],msg=f"Subject: Happy Birthday!\n\n{contents}")
    except Exception as e:
        print(f"Failed to send email: {e}")
