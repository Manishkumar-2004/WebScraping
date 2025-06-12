import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def solve_recaptcha(driver, logger):
    logger.info("Requesting reCAPTCHA token from anti-captcha service...")

    try:
        response = requests.get("http://216.48.184.36:4060/anti-captcha")
        response.raise_for_status()

        token = response.text.strip()
        if not token.startswith("03"):
            logger.error(f"Invalid reCAPTCHA token received: {token}")
            raise ValueError("Invalid reCAPTCHA token")

        logger.info("Token received. Waiting for reCAPTCHA textarea...")

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "g-recaptcha-response"))
        )

        logger.info("Injecting reCAPTCHA token into DOM...")

        driver.execute_script("""
            let textarea = document.getElementById("g-recaptcha-response");
            if (textarea) {
                textarea.style.display = 'block';
                textarea.value = arguments[0];
                textarea.dispatchEvent(new Event('change', { bubbles: true }));
            } else {
                console.error("reCAPTCHA textarea not found");
            }
        """, token)

        logger.info("reCAPTCHA token inserted successfully")
        time.sleep(3)

    except requests.RequestException as e:
        logger.error(f"Failed to fetch reCAPTCHA token: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during reCAPTCHA solving: {e}")
        raise
