from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os

Round_no = [1, 2, 3, 4, 5, 6]
year_no = [2016,2017,2018,2019,2020,2021,2022,2023]

# Path to the WebDriver executable
service = Service(executable_path = "chromedriver.exe")
driver = webdriver.Chrome(service = service)

def wait_and_display_element(element_id):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_id)))
        driver.execute_script(f"document.getElementById('{element_id}').style.display='block';")
    except Exception as e:
        print(f"Error: {e}")

try:
    for i in range(len(year_no)):
        for j in range(len(Round_no)):
            # Open the JoSAA website
            if year_no[i] != 2023:
                driver.get("https://josaa.admissions.nic.in/applicant/seatmatrix/OpeningClosingRankArchieve.aspx")
                year_element_id = "ctl00_ContentPlaceHolder1_ddlYear"
                wait_and_display_element(year_element_id)
                year_element = driver.find_element(By.ID, year_element_id)
                select = Select(year_element)
                select.select_by_value(str(year_no[i]))
            else:
                driver.get("https://josaa.admissions.nic.in/Applicant/seatallotmentresult/currentorcr.aspx")

            

            round_element_id = "ctl00_ContentPlaceHolder1_ddlroundno"
            wait_and_display_element(round_element_id)
            round_element = driver.find_element(By.ID, round_element_id)
            select = Select(round_element)
            select.select_by_value(str(Round_no[j]))

            instype_id = "ctl00_ContentPlaceHolder1_ddlInstype"
            wait_and_display_element(instype_id)
            instype = driver.find_element(By.ID, instype_id)
            select = Select(instype)
            select.select_by_value("ALL")

            insname_id = "ctl00_ContentPlaceHolder1_ddlInstitute"
            wait_and_display_element(insname_id)
            insname = driver.find_element(By.ID, insname_id)
            select = Select(insname)
            select.select_by_value("ALL")

            Academic_id = "ctl00_ContentPlaceHolder1_ddlBranch"
            wait_and_display_element(Academic_id)
            academic = driver.find_element(By.ID, Academic_id)
            select = Select(academic)
            select.select_by_value("ALL")

            if year_no[i] == 2023:
                Seat_type_id = "ctl00_ContentPlaceHolder1_ddlSeattype"
            else:
                Seat_type_id = "ctl00_ContentPlaceHolder1_ddlSeatType"
            wait_and_display_element(Seat_type_id)
            seat = driver.find_element(By.ID, Seat_type_id)
            select = Select(seat)
            select.select_by_value("ALL")

            Submit_id = "ctl00_ContentPlaceHolder1_btnSubmit"
            submit_element = driver.find_element(By.ID, Submit_id)
            submit_element.click()

            # Wait for the table to be present
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "table"))
            )

            # Get the page source and parse it with BeautifulSoup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')

            # Locate the table in the parsed HTML
            table = soup.find('table', class_="table table-bordered table-sm w-100 fs-7")

            # Check if the table was found
            if table is None:
                print("Table not found!")
            else:
                # Extract headers
                headers = [header.text.strip() for header in table.find_all('th')]

                # Extract rows
                rows = []
                for row in table.find_all('tr'):
                    cells = row.find_all('td')
                    if cells:
                        rows.append([cell.text.strip() for cell in cells])

                # Create a DataFrame
                df = pd.DataFrame(rows, columns=headers)

                # Save DataFrame to CSV
                file_name = f'table_data_round_{Round_no[j]}_year_{year_no[i]}.csv'
                df.to_csv(file_name, index=False)
                print(f"Saved {file_name}")

finally:
    # Close the web driver
    driver.quit()


dfs = []

for i in range(len(year_no)):
    for j in range(len(Round_no)):
        # Construct the path to the CSV file
        file_path = f"table_data_round_{Round_no[j]}_year_{year_no[i]}.csv"
        
        # Check if the file exists before reading
        if os.path.exists(file_path):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            
            # Add year and round columns
            df['Year'] = year_no[i]
            df['Round'] = Round_no[j]
            
            # Append the DataFrame to the list
            dfs.append(df)
        else:
            print(f"File '{file_path}' not found.")

# Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

combined_df.to_csv("combined.csv", index=False)
