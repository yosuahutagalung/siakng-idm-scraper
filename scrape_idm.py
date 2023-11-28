# References
# https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25
# https://iqss.github.io/dss-webscrape/filling-in-web-forms.html
# Bot SIAK Hocky Yudhiono
# https://www.browserstack.com/guide/download-file-using-selenium-python
# https://stackoverflow.com/questions/43149534/selenium-webdriver-how-to-download-a-pdf-file-with-python
# https://www.codingem.com/python-download-file-from-url/

from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import requests
from getpass import getpass
from rich import print
from rich.console import Console

LOGIN_URL = 'https://academic.ui.ac.id/main/Authentication/'
IDM_URL = "https://academic.ui.ac.id/main/Student/IDMView"
console = Console()


def get_idm_from_siak(username, password):
    # Setting up webdriver in incognito mode
    console.log('Initiating Selenium webdriver...')
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)

    # Login using credentials
    console.log('Logging in to SIAK...')
    driver.get(LOGIN_URL)

    u_field = driver.find_element(By.NAME, 'u')
    u_field.clear()
    u_field.send_keys(username)
    time.sleep(0.5)

    p_field = driver.find_element(By.NAME, 'p')
    p_field.clear()
    p_field.send_keys(password)
    time.sleep(0.5)

    driver.find_element(By.XPATH, "//input[@value='Login']").click()
    time.sleep(2)

    # Go to IDM Page and get download link
    console.log('Getting IDM download link...')
    driver.get(IDM_URL)
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//input[@value='Cetak IDM']").click()
    time.sleep(0.5)

    download_link = driver.find_element(
        By.XPATH, '//a[1]').get_attribute('href')
    driver
    driver.quit()

    # Download PDF from link
    console.log('Downloading IDM file...')
    response = requests.get(download_link)

    # Write to file
    file_name = username + '_idm.pdf'
    with open(file_name, 'wb') as pdf_file:
        pdf_file.write(response.content)

    console.log('Done!')
    time.sleep(1)
    console.log('File saved to ' + file_name)


if __name__ == '__main__':
    print('[bold green]=========================[/bold green]')
    print('Get your [bold blue]IDM[/bold blue] from [bold yellow]SIAKNG[/bold yellow]!')
    print('[bold green]=========================[/bold green]')

    username = input('Username: ')
    password = getpass()

    get_idm_from_siak(username, password)

