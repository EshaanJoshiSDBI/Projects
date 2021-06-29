from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#print('1. DataBase Management System')
DBMS_url = 'https://learning.sdbi.in/b/s-d-rvo-lkl-3or'
browser = webdriver.Chrome('/usr/bin/chromedriver')
browser.get(DBMS_url)
sign_in_button = browser.find_element_by_xpath('/html/body/div[1]/div/div/div/a')
sign_in_button.click()
email_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID,'identifierId')))
email_button.send_keys('your email(except the .sdbi.in)')
next_button = browser.find_element_by_id('identifierNext').click()
password_button = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,'password')))
password_button = password_button.find_element_by_tag_name('input')
password_button.send_keys('your password')
next_button = browser.find_element_by_id('passwordNext').click()
join_button = WebDriverWait(browser,100).until(EC.presence_of_element_located((By.ID,'room-join')))
join_button.click()
#room-join
