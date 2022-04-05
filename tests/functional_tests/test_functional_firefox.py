from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLogin:
    def test_login_firefox_success(self):
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        driver.get("http://127.0.0.1:5000/")
        assert "GUDLFT" in driver.title
        driver.find_element(By.NAME, "email").send_keys(
            "john@simplylift.co" + Keys.RETURN
        )
        WebDriverWait(driver, timeout=1).until(EC.title_contains("Summary"))
        assert "Summary" in driver.title
        driver.quit()

    def test_login_firefox_wrong_email_should_fail(self):
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        driver.get("http://127.0.0.1:5000/")
        assert "GUDLFT" in driver.title
        driver.find_element(By.NAME, "email").send_keys("wrong@email.fr" + Keys.RETURN)
        WebDriverWait(driver, timeout=1).until(EC.title_contains("GUDLFT"))
        assert "Sorry, that email wasn't found." in driver.page_source
        driver.quit()
