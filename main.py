import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def main():
    f = open("cpfs.txt", "r")
    cpfs = f.readlines()
    o = open('output.txt', 'w+')
    options = uc.ChromeOptions()
    options.headless=True
    driver = uc.Chrome(options=options)
    for cpf in cpfs:
         try:
            c=''
            print("pesquisando no PJE "+cpf.strip())
            driver.get("https://www.jusbrasil.com.br/")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="autocomplete-input"]')))
            gs = driver.find_element(By.XPATH, '//*[@id="autocomplete-input"]')
            gs.click()
            gs.clear()
            for key in cpf.strip():
                gs.send_keys(key)
            driver.find_element(By.XPATH, '/html/body/div[2]/div/header/form/div/div[2]/button/span').click()
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/main/ul')))
                t=driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/main/ul')
                rows = t.find_elements(By.TAG_NAME, "li")
                for row in rows:
                    if "TRF" in str(row.find_element(By.TAG_NAME, "a").text):
                        c+=str(row.find_element(By.TAG_NAME, "a").text)+"; "
                        print('encontrado')
            except:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/main/div[2]/div/p')))
                if 'Nenhum' in driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/main/div[2]/div/p').text:
                    print("sem processo de teto")
                else:
                    raise Exception('')
            o.write(cpf.strip()+";"+c.strip()+"\n")
         except:
             o.write(cpf.strip()+",erro\n")
             print('erro encontrado, pulando cpf: '+cpf)
             pass

if __name__ == '__main__':
    main()
