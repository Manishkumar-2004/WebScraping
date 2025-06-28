from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def perform_login(driver, wait, cred, solve_recaptcha, logger):
    driver.get("https://visaforazerbaijan.org.uk/my-account/")
    logger.info("Navigated to login page")

    try:
        cookie_accept = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.cmplz-btn.cmplz-accept")))
        cookie_accept.click()
        logger.info("Cookie banner accepted")
    except TimeoutException:
        logger.info("No cookie banner found or already accepted")

    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(cred["username"])
    logger.info("Username entered successfully")

    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(cred["password"])
    logger.info("Password entered successfully")

    solve_recaptcha(driver,logger)

    try:
        checkbox = driver.find_element(By.ID, "rememberme")
        if not checkbox.is_selected():
            checkbox.click()
        logger.info("Remember me checkbox clicked")
    except Exception as e:
        logger.warning(f"Remember me checkbox issue: {e}")

    wait.until(EC.element_to_be_clickable((By.NAME, "login"))).click()
    logger.info("Login button clicked, waiting for dashboard...")
