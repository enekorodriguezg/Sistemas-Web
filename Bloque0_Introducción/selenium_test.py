# -*- coding: UTF-8 -*-


from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time


def selenium_test():
    uri = "https://www.google.com/search?q=ehu"

    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

    print("Openning the browser...")
    browser = webdriver.Firefox(options=options)

    print("Openning the webpage...")
    browser.get(uri)

    print("Waiting 5s...")
    time.sleep(5)

    print("Closing the browser...")
    browser.close()


if __name__ == '__main__':
    selenium_test()

