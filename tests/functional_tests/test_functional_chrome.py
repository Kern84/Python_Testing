from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestUserExperience:
    def test_login_chrome_sucess(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.maximize_window()
        driver.get("http://127.0.0.1:5000/")
        assert "GUDLFT" in driver.title
        driver.find_element(By.NAME, "email").send_keys(
            "john@simplylift.co" + Keys.RETURN
        )
        WebDriverWait(driver, timeout=1).until(EC.title_contains("Summary"))
        assert "Summary" in driver.title
        driver.quit()  # no because of succession off actions

    def test_login_chrome_wrong_email_should_fail(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.maximize_window()
        driver.get("http://127.0.0.1:5000/")
        assert "GUDLFT" in driver.title
        driver.find_element(By.NAME, "email").send_keys("wrong@email.fr" + Keys.RETURN)
        WebDriverWait(driver, timeout=1).until(EC.title_contains("GUDLFT"))
        assert "Sorry, that email wasn't found." in driver.page_source
        driver.quit()  # no because of succession off actions


# TODO create a function for the user experience with every function needed
