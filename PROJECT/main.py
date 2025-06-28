# main.py

import json
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from log_manager import setup_logger
from login import perform_login
from utils.recaptcha_solver import solve_recaptcha
from utils.drop_file import drop_file
from application_form import fill_application

def run_automation_from_dict(cred: dict, logger):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Uncomment if running on server
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        perform_login(driver, wait, cred, solve_recaptcha, logger)
        fill_application(driver, wait, cred, drop_file, logger)
        logger.info("Visa application completed successfully")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        driver.quit()

def main():
    logger = setup_logger()
    logger.info("Visa automation script started")

    json_path = os.path.join(os.path.dirname(__file__), "apply.json")
    with open(json_path, "r", encoding="utf-8") as f:
        cred = json.load(f)

    run_automation_from_dict(cred, logger)

if __name__ == "__main__":
    main()
