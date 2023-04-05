from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import configparser
import PDCEvent

PDCURL = "https://w5.hkust-gz.edu.cn/cgi-bin/std_cgi.sh/WService=broker_za_p/prg/akdc_stdt_main.r"
SUFFIX = "@connect.hkust-gz.edu.cn"

        

def readUserInfo(path):
    configReader = configparser.ConfigParser()
    configReader.read(path)
    userInfo = {"username": configReader.get("INFO", "username"), "password": configReader.get("INFO", "password")}
    return userInfo

def loginAndNavigation(userDataPath):
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(PDCURL)

    # Selectors for the element finding
    emailFieldSelector = (By.ID, "i0116")
    pwdFieldSelector = (By.ID, "i0118")
    nextBtnSelector = (By.ID, "idSIButton9")
    wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
    username, password = [readUserInfo(userDataPath)[key] for key in readUserInfo(userDataPath)]

    emailField = wait.until(EC.element_to_be_clickable(emailFieldSelector))
    nextBtn = wait.until(EC.element_to_be_clickable(nextBtnSelector))
    emailField.send_keys(username + SUFFIX)
    nextBtn.click()


    pwdField = wait.until(EC.element_to_be_clickable(pwdFieldSelector))
    signInBtn = wait.until(EC.element_to_be_clickable(nextBtnSelector))
    pwdField.send_keys(password)  
    signInBtn.click()

    # Navigate to the event schedule page, cooperating with frames
    detailFrame = driver.find_element(By.XPATH, "//frame[@name = 'detail_frame']")
    driver.switch_to.frame(detailFrame)
    eventEnquiryAnchor = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.LINK_TEXT, "Event Schedule Enquiry"))
    eventEnquiryAnchor.click()

    scheduleFrame = driver.find_element(By.XPATH, "//frame[@name = 'detail_frame']")
    driver.switch_to.frame(scheduleFrame)
    searchButton = driver.find_element(By.XPATH, "//input[@name = 'f_searchBtn']")
    searchButton.click()

    eventTableFrame = driver.find_element(By.XPATH, "//frame[@name = 'detail_frame']")
    driver.switch_to.frame(eventTableFrame)
    
    return driver.page_source

    


def dataProcessing(dataHTML):
    soup = BeautifulSoup(dataHTML)
    eventTable = soup.find_all("table", class_ = "TB-4-OUTER-1")[-1]
    events = eventTable.find_all("tr", class_ = re.compile("TR-4-DETAIL.*"))

    eventMetaInfoArr = []
    for idx, event in enumerate(events):
        # odd index represents a remark td
        if(idx % 2 != 0):
            # TODO: deal with remark here
            continue
        metaInfo = [el.text for el in event.find_all("td", class_ = re.compile("TD.*DETAIL"))]
        eventMetaInfoArr.append(metaInfo)

    return eventMetaInfoArr