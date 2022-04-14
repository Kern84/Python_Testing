from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_user_experience_firefox():
    """
    Function to test the user experience.
    Go to the site index page;
    Click on the link to go to the club points page (user not logged in);
    Return to the index page;
    Try to log in with a wrong email;
    Log in with a correct email;
    Click on the link to go to the club points page (user logged in);
    Return to the showSummary page;
    Click on the link to go to the booking page;
    Book 4 places for the competition;
    Logout.
    """
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.maximize_window()
    driver.get("http://127.0.0.1:5000/")
    WebDriverWait(driver, timeout=1).until(EC.title_contains("GUDLFT"))
    assert "GUDLFT" in driver.title

    club_points_link = driver.find_element(By.LINK_TEXT, "See clubs")
    club_points_link.click()
    WebDriverWait(driver, timeout=1).until(EC.title_contains("Club Points"))
    assert "Club Points" in driver.title

    driver.back()
    WebDriverWait(driver, timeout=1).until(EC.title_contains("GUDLFT"))
    assert "GUDLFT" in driver.title

    driver.find_element(By.NAME, "email").send_keys("wrong@email.fr" + Keys.RETURN)
    WebDriverWait(driver, timeout=1).until(EC.title_contains("GUDLFT"))
    assert "Sorry, that email" in driver.page_source

    driver.find_element(By.NAME, "email").send_keys("john@simplylift.co" + Keys.RETURN)
    WebDriverWait(driver, timeout=1).until(EC.title_contains("Summary"))
    assert "Summary" in driver.title

    club_points_log_in_link = driver.find_element(By.LINK_TEXT, "See clubs")
    club_points_log_in_link.click()
    WebDriverWait(driver, timeout=1).until(EC.title_contains("Club Points"))
    assert "Club Points" in driver.title

    driver.back()
    WebDriverWait(driver, timeout=1).until(EC.title_contains("Summary"))
    assert "Summary" in driver.title

    book_places_link = driver.find_element(By.LINK_TEXT, "Book Places")
    book_places_link.click()
    WebDriverWait(driver, timeout=1).until(EC.title_contains("Booking for"))
    assert "Booking for" in driver.title

    register_places = driver.find_element(By.NAME, "places")
    register_places.send_keys("1")
    validate_choice = driver.find_element(By.TAG_NAME, "button")
    validate_choice.click()
    WebDriverWait(driver, timeout=1).until(EC.title_contains("Summary"))
    assert "Great-booking complete!" in driver.page_source

    logout_link = driver.find_element(By.LINK_TEXT, "Logout")
    logout_link.click()
    WebDriverWait(driver, timeout=1).until(EC.title_contains("GUDLFT"))
    assert "GUDLFT" in driver.title

    driver.quit()
