from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os
service = Service(executable_path = "chromedriver.exe")
driver = webdriver.Chrome(service = service)
driver.get("https://josaa.admissions.nic.in/applicant/seatmatrix/seatmatrixinfo.aspx")
submit_element = driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_btnSubmit')
submit_element.click()
page_source = driver.page_source
soup = BeautifulSoup(page_source,'lxml')
table = soup.find('table', class_="table table-bordered table-sm w-100 fs-7")
headers = [header.text.strip() for header in table.find_all('th')]
exclude_column_name = {'Program-Total','Seat Capacity','Female Supernumerary'}
if exclude_column_name in headers:
    exclude_index = headers.index(exclude_column_name)
    headers.pop(exclude_index)
# Extract rows
rows = []
for row in table.find_all('tr'):
    cells = row.find_all('td')
    if cells:
        row_data = [cell.text.strip() for i, cell in enumerate(cells) if i != exclude_index]
        rows.append(row_data)

# Create a DataFrame
df = pd.DataFrame(rows, columns=headers)
df.to_csv("Seat_State_matrix.csv",index=False)
print(df)