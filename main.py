from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from paths import pathLib
import time
import random

user = input('Enter Username: ')
pwd = input('Enter Password: ')

url = 'https://open.spotify.com/'

driver = webdriver.Chrome()
driver.get(url)
page = driver.page_source

data = BeautifulSoup(page, 'html.parser')   

def login(username, password):

    # Go to login page
    ActionChains(driver).click(
        driver.find_element_by_xpath(pathLib['LOGIN_PAGE'])
    ).perform()

    # Wait until new page is available
    while True:
        try:
            driver.find_element_by_xpath(pathLib['USERNAME_BOX'])
            break
        except: time.sleep(3)

    time.sleep(random.uniform(0.1, 0.2))

    # Fill email address
    for char in username:
        ActionChains(driver).send_keys_to_element(
            driver.find_element_by_xpath(pathLib['USERNAME_BOX']),
            char
        ).perform()

        time.sleep(random.uniform(0.05, 0.15))

    time.sleep(random.uniform(0.1, 0.2))

    # Fill password
    for char in password:
        ActionChains(driver).send_keys_to_element(
            driver.find_element_by_xpath(pathLib['PASSWORD_BOX']),
            char
        ).perform()

        time.sleep(random.uniform(0.05, 0.15))

    time.sleep(random.uniform(0.1, 0.2))

    # Click on login button
    ActionChains(driver).click(
        driver.find_element_by_xpath(pathLib['LOGIN_BUTTON'])
    ).perform()

def isMute():
    for tag in data.find_all('button'):
        try: tag.get('class')
        except: continue
        if not 'volume-bar__icon-button' in tag.get('class'): continue

        if 'Mute' in tag.get('aria-label'): return False
        else: return True

def isAdvertisement():
    for tag in data.find_all('footer'):
        try: tag.get('data-testadtype')
        except: continue

        if 'ad-type-none' in tag.get('data-testadtype'): return False
        else: return True

login(user, pwd)

while True:
    time.sleep(0.2)

    pbPos = driver.find_element_by_xpath(
        pathLib['PLAYBACK_POSITION']).text
    pbDur = driver.find_element_by_xpath(
        pathLib['PLAYBACK_DURATION']).text

    if pbPos == pbDur:
        while pbPos != pbDur:
            pbPos = driver.find_element_by_xpath(
            pathLib['PLAYBACK_POSITION']).text
            pbDur = driver.find_element_by_xpath(
            pathLib['PLAYBACK_DURATION']).text
            time.sleep(0.2)

        isA = isAdvertisement()
        isM = isMute()

        if isA and not isM:
            ActionChains(driver).click(
                driver.find_element_by_xpath(pathLib['MUTE_BUTTON'])
            ).perform()
        elif not isA and isM:
            ActionChains(driver).click(
                driver.find_element_by_xpath(pathLib['MUTE_BUTTON'])
            ).perform()