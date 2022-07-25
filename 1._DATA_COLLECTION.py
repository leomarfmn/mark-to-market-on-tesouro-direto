from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import pandas as pd

# ACCESSES WEBSITE
PATH = "/Users/leomarfonseca/Downloads/chromedriver-2"
driver = webdriver.Chrome(PATH)
driver.get("https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm")


# CLOSES COOKIES
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-close-btn-container"]/button'))).click() 
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'perfil-notice__close'))).click() 


# FINDS AND FILTERS DATA
elements1 = driver.find_elements(By.CLASS_NAME, 'td-invest-table__name__text')  # Finds all títulos
elements2 = driver.find_elements(By.CLASS_NAME, 'td-invest-table__col__text')   # Finds data about all titulos, including the hidden ones
elements2 = [x.text for x in elements2 if len(x.text) > 0]                      # Filters out the data from the hidden títulos
elements2 = [elements2[n : n + 4] for n in range(0, len(elements2), 4)]         # Groups the data from the títulos
elements1 = elements1[ : len(elements2)]                                        # Filters out the hidden títulos


# CREATED AND SAVES DATAFRAME
df = pd.DataFrame(columns = ['TÍTULO','TAXA', 'VALOR MÍNIMO', 'VALOR TÍTULO', 'VENCIMENTO'])
for i in range(len(elements1)):
    df.loc[i, 'TÍTULO'] = elements1[i].text.replace('\n', ' ')
    df.loc[i, 'TAXA'] = elements2[i][0]
    df.loc[i, 'VALOR MÍNIMO'] = elements2[i][1]
    df.loc[i, 'VALOR TÍTULO'] = elements2[i][2]
    df.loc[i, 'VENCIMENTO'] = elements2[i][3]
df['VENCIMENTO'] = pd.to_datetime(df['VENCIMENTO'])
#print(df.info())
df.to_csv('df.csv')
    

# CLOSES BROWSER
driver.quit()