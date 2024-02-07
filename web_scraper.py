from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service #THIS IS FOR FIREFOX, CHANGE AS NEEDED (IF YOU ARE USING CHROME ETC...)
from selenium.webdriver.firefox.options import Options #THIS IS FOR FIREFOX, CHANGE AS NEEDED (IF YOU ARE USING CHROME ETC...)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image, ImageChops
from email_sender import send_email

def compare_images(img1_path, img2_path):
    """
    Compare two images and return True if they are the same.
    """
    with Image.open(img1_path) as img1, Image.open(img2_path) as img2:
        diff = ImageChops.difference(img1, img2)
        if diff.getbbox() is None:
            # Images are the same
            return True
        else:
            # Images are different
            return False

webdriver_path = "PATH_TO_YOUR_WEBDRIVER"
s = Service(webdriver_path)
option = Options()
option.add_argument("-headless")
driver = webdriver.Firefox(service=s, options=option) #THIS IS FOR FIREFOX, CHANGE AS NEEDED (IF YOU ARE USING CHROME ETC...)
login_url = "https://accommodation.fmel.ch/StarRezPortal/6d85dab14921fe4132a13a0464309f7503f9013c9668de0ef80310ac66f6ab87e34ea350e5231d1f51cc5a1a6aa8d2cef3bd093a6edba838c444501c789051a5/7/8/Login-Login?IsContact=False"

username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"

driver.get(login_url)

delay = 10
loaded = False

while loaded == False:
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, "Username")))
        print("[+] Login page loaded!")

        driver.find_element(By.NAME, "Username").send_keys(username)
        driver.find_element(By.NAME, "Password").send_keys(password)
        driver.find_element(By.XPATH, '//button[@class="cc-btn cc-allow cookie-button"]').click()
        driver.find_element(By.XPATH, '//button[@aria-label="Login"]').click()

        loaded = True
    except TimeoutException:
        print("[!] Page is too slow to load, trying again...")

login_success = False
while login_success == False:
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//a[@class="nav-right-item logout nav-item ui-logout"]')))
        print("[+] Login Successful!")
        login_success = True
    except TimeoutException:
        print("[!] Login Failed! Trying again!")
        driver.find_element(By.NAME, "Password").send_keys(password)
        driver.find_element(By.XPATH, '//button[@aria-label="Login"]').click()
        
element = driver.find_element(By.XPATH, "//article[@class='page-content ui-page-article ui-ignore-scroll-datetime-picker']")

current_screenshot = element.screenshot("current.png")

if compare_images('./baseline.png', "./current.png"):
    print("Nothing changed!")
else:
    print("Something changed!")
    send_email("./current.png")

driver.close()