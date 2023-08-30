import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

DOCS_URL = "https://docs.google.com/PATH"

ZILLOW_URL = "https://www.zillow.com/PATH"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                  "114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8"
}
CHROME_DRIVER_PATH = r"D:\Documents\Laura\100_days_coding\chromedriver_win32\chromedriver.exe"
SERVICE = Service(CHROME_DRIVER_PATH)

driver = webdriver.Chrome(service=SERVICE)
driver.get(DOCS_URL)
time.sleep(3)

#Getting all properties
# scroll = driver.find_element(By.XPATH, '//*[@class="srp-page-container"]')
# for i in range(10):
#     driver.execute_script(f"arguments[0].scrollTop = {i*1000}", scroll)
#     time.sleep(1)

response = requests.get(ZILLOW_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
all_links = soup.find_all(name="a", class_="property-card-link")
property_link = []
for link in all_links:
    href = link.get('href')
    if "http" not in href:
        property_link.append(f"https://www.zillow.com{href}")
    else:
        property_link.append(href)
print(property_link)
all_prices = soup.find_all(name="div", class_="gKmVGs")
property_price = [price.getText() for price in all_prices]
print(property_price)
all_addresses = soup.find_all(name="address")
property_address = [address.getText().split(" | ")[-1] for address in all_addresses]
print(property_address)

for info in range(len(all_links)):
    doc_address = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/'
                                                         'div/div[1]/div/div[1]/input')
    doc_address.send_keys(property_address[info])
    time.sleep(1)
    doc_price = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/'
                                                       'div[1]/div/div[1]/input')
    doc_price.send_keys(property_price[info])
    time.sleep(1)
    doc_link = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/'
                                                      'div[1]/div/div[1]/input')
    doc_link.send_keys(property_link[info])
    time.sleep(1)
    submit = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    submit.click()
    time.sleep(1)
    another_response = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    another_response.click()
    time.sleep(1)
