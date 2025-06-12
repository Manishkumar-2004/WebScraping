from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

def fill_application(driver, wait, cred, drop_file, logger):
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/apply/') and contains(text(), 'Apply Now')]"))).click()
    logger.info("Clicked 'Apply Now' button")

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/product/standard-evisa/')]"))).click()
    logger.info("Clicked 'Standard eVisa' link")

    # Step 1
    Select(wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_6509b31de9a64]")))).select_by_value(cred["nationality"])
    logger.info("Nationality selected")

    Select(wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650d6cdecc381]")))).select_by_value(cred["passport"])
    logger.info("Passport type selected")

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.wapf_btn_next"))).click()
    logger.info("Moved to Step 2")

    # Step 2
    Select(wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650d6dbdb9db3]")))).select_by_value(cred["purpose"])
    logger.info("Purpose of visit selected")

    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('change'));
    """, wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650df9e3e84f1]"))), cred["date"])
    logger.info("Date of arrival entered")

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.wapf_btn_next"))).click()
    logger.info("Moved to Step 3")

    # Step 3
    wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650d768122452]"))).send_keys(cred["surname"])
    logger.info("Surname entered")

    wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650d76d1545cc]"))).send_keys(cred["other_name"])
    logger.info("Other name entered")

    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('change'));
    """, wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650d76f51313f]"))), cred["dob"])
    logger.info("DOB entered")

    Select(wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650d773085c3d]")))).select_by_value(cred["cob"])
    logger.info("Country of birth selected")

    wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650dfac3aa534]"))).send_keys(cred["pob"])
    logger.info("Place of birth entered")

    Select(wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650dfaeefa587]")))).select_by_value(cred["sex"])
    logger.info("Sex selected")

    Select(wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650dfb2272ee8]")))).select_by_value(cred["occupation"])
    logger.info("Occupation selected")

    wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_651159a2ddd15]"))).send_keys(cred["mobileno"])
    logger.info("Mobile number entered")

    wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_65115a1889505]"))).send_keys(cred["address"])
    logger.info("Address entered")

    wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_65115a4dca349]"))).send_keys(cred["email"])
    logger.info("Email entered")

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.wapf_btn_next"))).click()
    logger.info("Moved to Step 4")

    wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_651167afed118]"))).send_keys(cred["passportNo"])
    logger.info("Passport number entered")

    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('change'));
    """, wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_651168085f7e4]"))), cred["passportIssueDate"])
    logger.info("Passport issue date entered")

    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('change'));
    """, wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_651168410fb3e]"))), cred["passportExpiryDate"])
    logger.info("Passport expiry date entered")

    drop_target = wait.until(EC.presence_of_element_located((By.ID, "wapf-dz-65116994dec8e")))
    drop_file(driver, drop_target, cred["image_path"], logger)

    wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_65116a8a184b1]"))).send_keys(cred["azb_address"])
    logger.info("Azerbaijan address entered")

    checkbox = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@type='checkbox' and contains(@name, '650d75f5637e6')]")))
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", checkbox)
    logger.info("Declaration checkbox clicked")

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.single_add_to_cart_button"))).click()
    logger.info("Final submit button clicked")
