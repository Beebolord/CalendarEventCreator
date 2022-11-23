from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.common.by import By


def function():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'C:\geckodriver.exe')
    driver.get("https://google.com")
    print("Headless Firefox Initialized")
    title = driver.find_element(By.XPATH("/html/body/div[1]/div[2]/div/img"))
    print(title.text)
    driver.quit()


def snakeScraper():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'C:\geckodriver.exe')
    driver.get("https://virtuo.ciussscn.rtss.qc.ca/portals/home/app/login")
    driver.maximize_window()
    time.sleep(1.5)
    print(driver.title)

    driver.find_element(By.XPATH, "/html/body/app-root/div/ms-navigation/div/div/app-home-login/div/div/div[3]/div["
                                 "2]/div[2]/div[2]/a").click()
    time.sleep(1.5)

    driver.find_element(By.ID,"username-txt").click()
    driver.find_element(By.ID,"username-txt").send_keys("510217")

    driver.find_element(By.ID, "password-txt").click()
    driver.find_element(By.ID,"password-txt").send_keys("Soleil12+")
    # Enter
    time.sleep(3)
    driver.find_element(By.XPATH,
        "/html/body/app-root/div/ms-navigation/div/div/app-home-login/div/div/div[3]/div[2]/ms-form/form/dx-validation-group/div[2]/ms-button/div/ms-default-button/button").click()
    time.sleep(4)
    print(driver.current_url)
    print(driver.title)
    driver.quit()


if __name__ == '__main__':
   snakeScraper()
