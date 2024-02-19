from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver.exe'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


# this ensures that the code is not runned when this module is imported.
if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('https://www.github.com/Gabrielxdf/')
    sleep(5)
    browser.quit()
