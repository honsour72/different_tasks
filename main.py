from selenium import webdriver
import time, os,  datetime, pandas as pd

# функция, возвращающая данные с текущей страницы
def collect_data_from_page():
    data_from_page = []
    for i in range(1, 101):
        try:
            chrome.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div/div[{}]/div[6]/span[1]/span/span[1]'.format(i)).click()
            time.sleep(1)
            company = chrome.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/div/div[3]/div/div[2]/div/div[3]/div/div/div[{}]/div[3]/div[1]/a'.format(i)).text
            for j in range(1, 101):
                try:
                    n1_str = chrome.find_element_by_xpath('/html/body/div[{}]/div/div/div/div/div[2]/span'.format(j)).text
                    time.sleep(1)
                    n1_fio = chrome.find_element_by_xpath('/html/body/div[{}]/div/div/div/div/div[1]'.format(j)).text
                    n1_email = chrome.find_element_by_xpath('/html/body/div[{}]/div/div/div/div/div[4]/a'.format(j)).text
                    ready = [n1_fio, company, n1_email, n1_str]
                    data_from_page.append(ready)
                except:
                    pass
        except:
            pass
    return data_from_page

profession = 'товародвижение'

chrome = webdriver.Chrome()
# print(dir(chrome))
chrome.maximize_window()
chrome.get("https://hh.ru/")
find = chrome.find_element_by_xpath('/html/body/div[5]/div[2]/div/div[1]/div[3]/div/div/form/div/div[1]/div/input')
find.send_keys(profession)
chrome.find_element_by_xpath('/html/body/div[5]/div[2]/div/div[1]/div[3]/div/div/form/div/div[2]/button').click()
time.sleep(4)

all_data = collect_data_from_page()

amount_of_pages = int(chrome.find_element_by_css_selector("body > div.HH-MainContent.HH-Supernova-MainContent > div > div > div.bloko-columns-wrapper > div > div.sticky-container > div > div.vacancy-serp-wrapper.HH-SearchVacancyDropClusters-XsHiddenOnClustersOpenItem > div > div.bloko-gap.bloko-gap_top > div > span.bloko-button-group > span:nth-child(3) > a").text)
next_page = chrome.current_url + "?page=" + '1'
for page in range(2, amount_of_pages):
    chrome.get(next_page)
    data_from_current_page = collect_data_from_page()
    all_data.extend(data_from_current_page)
    next_page = next_page.replace(next_page[-1], str(page))

chrome.close()

df = pd.DataFrame(all_data, columns=["Имя", "Эл. почта", "Номер телефона", "Должность и компания"])
current_date = str(datetime.date.today())
df.to_csv('Результаты по запросу на вакансию {} за {}.csv'.format(profession, current_date))


