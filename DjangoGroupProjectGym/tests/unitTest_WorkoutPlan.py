

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):
        driver = self.driver
        driver.maximize_window()
        user = "mem1"
        pwd = "qwertyuiopASDFGHJKL"
        driver.get("http://127.0.0.1:8000/")
        time.sleep(3)
        driver.find_element(By.XPATH, "//a[contains(., 'Login')]").click()
        elem = driver.find_element(By.ID,"id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID,"id_password")
        elem.send_keys(pwd)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)

        driver.find_element(By.XPATH, "//a[contains(., 'Dashboard')]").click()
        driver.find_element(By.XPATH, "//a[contains(., 'Workout Plan')]").click()

        time.sleep(5)
        try:
            elements = driver.find_elements(By.XPATH, "//button[normalize-space()='Log Workout Progress']")

        except NoSuchElementException:
            driver.close()
            self.fail("Dashboard page not found")

        time.sleep(2)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
