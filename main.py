from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from paths import pathLib
import time
import random

#user = input('Enter Username: ')
#pwd = input('Enter Password: ')

url = 'https://open.spotify.com/'

driver = webdriver.Chrome()
driver.get(url)

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

#login(user, pwd)

while True:
    time.sleep(0.1)

    try:
        Advertisement = driver.find_element(
            By.XPATH, pathLib['TRACK_BAR']).get_attribute('data-testadtype')
        Mute = driver.find_element(
            By.XPATH, pathLib['MUTE_BUTTON']).get_attribute('aria-label')

        pbDur = driver.find_element(
            By.XPATH, pathLib['PLAYBACK_DURATION']).text
        pbPos = driver.find_element(
            By.XPATH, pathLib['PLAYBACK_POSITION']).text
    except: continue

    absDur = (int(pbDur.split(':')[0]) * 60) + (int(pbDur.split(':')[1]))
    absPos = (int(pbPos.split(':')[0]) * 60) + (int(pbPos.split(':')[1]))

    if absDur > 5 and (absDur - absPos) > 5:
        time.sleep(absDur - absPos)

    if Advertisement == 'ad-type-none': isAdvertisement = False
    else: isAdvertisement = True
    if Mute == 'Mute': isMute = False
    else: isMute = True

    if isAdvertisement and not isMute:
        ActionChains(driver).click(
            driver.find_element_by_xpath(pathLib['MUTE_BUTTON'])
        ).perform()
    elif not isAdvertisement and isMute:
        ActionChains(driver).click(
            driver.find_element_by_xpath(pathLib['MUTE_BUTTON'])
        ).perform()
