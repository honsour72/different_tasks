import pandas as pd
from selenium import webdriver
import time
import sqlite3

def get_data_from_page():
    all_data_from_page = []
    all_data_from_page_for_db = []
    for i in range(1, 71):
        try:
            show_contacts_button_xpath = "/html/body/div[6]/div/div/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div/div[{}]/div[6]/span[1]/span/span[1]".format(i)                                      
            show_contacts_button       = browser.find_element_by_xpath(show_contacts_button_xpath)
            show_contacts_button.click()
            time.sleep(2)
            try:
                name_xpath    = "/html/body/div[8]/div/div/div/div/div[1]"
                number_xpath  = "/html/body/div[8]/div/div/div/div/div[2]/span"
                email_xpath   = "/html/body/div[8]/div/div/div/div/div[4]/a"
                company_xpath = "/html/body/div[6]/div/div/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div/div[{}]/div[3]/div[1]/a".format(i)
                name   = browser.find_element_by_xpath(name_xpath).text
                number = browser.find_element_by_xpath(number_xpath).text
                email  = browser.find_element_by_xpath(email_xpath).text
                company = browser.find_element_by_xpath(company_xpath).text                
                show_contacts_button.click()
                if number[3] == "9":
                    need_str = name + ","*28 + "* myContacts,* ," + email + ",," + number + ",," + company + ",,,,,"
                    body = need_str.split(",")
                    all_data_from_page.append(body)
                    body_for_db = [name, number, email, company]
                    all_data_from_page_for_db.append(body_for_db)
            except:
                show_contacts_button.click()
                pass
        except:
            pass
    return all_data_from_page, all_data_from_page_for_db

vacancy = "товародвижение"

# поиск по вакансии
browser = webdriver.Chrome("C:\Program Files\chromedriver_win32\chromedriver.exe")
browser.get("https://hh.ru")
search_field = browser.find_element_by_xpath("/html/body/div[5]/div[2]/div/div[1]/div[3]/div/div/form/div/div[1]/div/input")
search_field.send_keys(vacancy)
search_button = browser.find_element_by_xpath("/html/body/div[5]/div[2]/div/div[1]/div[3]/div/div/form/div/div[2]/button/span[2]").click()
time.sleep(2)

# сбор данных с первой страницы
all_data, all_data_for_db = get_data_from_page()

# переход по страницам

# pages_range = int(browser.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div/div[3]/div/div[2]/div/div[8]/div/span[3]/a").text)
pages_range = int(browser.find_element_by_xpath('//a[@class="bloko-button HH-Pager-Control"]').text)
start_url = browser.current_url

for page in range(1, 1):
    next_url = start_url + "&page=" + str(page)
    browser.get(next_url)
    all_data.extend(get_data_from_page()[0])
    all_data_for_db.extend(get_data_from_page()[1])
    time.sleep(2)

# закрытие браузера
browser.close()

# создание датафрейма
h  = "Name,Given Name,Additional Name,Family Name,Yomi Name,Given Name Yomi,Additional Name Yomi,Family Name Yomi,Name Prefix,Name Suffix,Initials,Nickname,Short Name,Maiden Name,Birthday,Gender,Location,Billing Information,Directory Server,Mileage,Occupation,Hobby,Sensitivity,Priority,Subject,Notes,Language,Photo,Group Membership,E-mail 1 - Type,E-mail 1 - Value,Phone 1 - Type,Phone 1 - Value,Organization 1 - Type,Organization 1 - Name,Organization 1 - Yomi Name,Organization 1 - Title,Organization 1 - Department,Organization 1 - Symbol,Organization 1 - Location,  Organization 1 - Job Description"
head = h.split(",")[:-1]
# head2 = list(map(lambda x: x+" text", head))

# запись в csv-файл для загрузки в гугл-контакты с распознаванием номера
df = pd.DataFrame(all_data, columns=head)
df = df.drop_duplicates(subset=["Name", "Phone 1 - Value"])
df.to_csv("result.csv", index = False)

# запись в бд
connection = sqlite3.connect('head_hunters.db')

cursor = connection.cursor()

# Create table
# correct_header = ", ".join(head2)
# execute_command = '''CREATE TABLE head_hunters ({})'''.format(correct_header)
execute_command = '''CREATE TABLE head_hunters (name text, number text, email text, company text)'''
cursor.execute(execute_command)

# Insert many rows of data
# q = ", ".join(["?"]*4)
# sql_statement = "INSERT INTO head_hunters VALUES ({})".format(q)
sql_statement = "INSERT INTO head_hunters VALUES (?, ?, ?, ?)"
for row in all_data_for_db:
    cursor.execute(sql_statement, row)

# Save (commit) the changes
connection.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
connection.close()

