from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import os
import time
import base64
import requests

def drop_file(driver, drop_target, file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        content = f.read()
    b64_content = base64.b64encode(content).decode()

    driver.execute_script(
        """
        var b64contents = arguments[0];
        var fileName = arguments[1];
        var target = arguments[2];

        function b64ToUint8Array(b64) {
            var binary_string = window.atob(b64);
            var len = binary_string.length;
            var bytes = new Uint8Array(len);
            for (var i = 0; i < len; i++) {
                bytes[i] = binary_string.charCodeAt(i);
            }
            return bytes;
        }

        var uint8Array = b64ToUint8Array(b64contents);
        var blob = new Blob([uint8Array], {type: 'image/jpeg'});
        var file = new File([blob], fileName, {type: 'image/jpeg'});

        var dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);

        var event = new DragEvent('drop', {
            dataTransfer: dataTransfer,
            bubbles: true,
            cancelable: true
        });

        target.dispatchEvent(event);
        """,
        b64_content,
        file_name,
        drop_target
    )


def main():
    # Load credentials from JSON
    json_path = os.path.join(os.path.dirname(__file__), 'apply.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        cred = json.load(f)

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    try:
        # Step 1: Go to login page
        driver.get("https://visaforazerbaijan.org.uk/my-account/")

        # Accept cookies if shown
        try:
            cookie_accept = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.cmplz-btn.cmplz-accept")))
            cookie_accept.click()
            print("Cookie banner accepted")
        except TimeoutException:
            print("No cookie banner found or already accepted")

        
        # Enter login credentials
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(cred["username"])
        wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(cred["password"])

        recaptcha_token = "03AFcWeA58DbceWcnnlkulivr7hgeuiDI8zgp9b0TCfLLKnccZK7OohAWrKS6ViYnvQI3ytxOAvK3ZHtxGyryy0H85-4LS9jqFcAFWdKCnJH2FkT9SznUjMOB-OaED-IsU54lHn7P_tIMokNiB-mI-cM73eyle4SSRdR2O7fGebMPoCinuR3urtF7niCr4ZOeC8n01IjrqKh6P1TsIf6HnQQ4q8qJngOMuAaAbHcdXslkAwh4NHQhfU_xNt89pJV6iWdKmxnnlG6Wtg5GsFN1GbKXExTzATf8UENiM0WI8JZvDr2UBqSA8O0STixam2aIN9YncIEfMw8vO1GwsMpxzxVTnRTqjl3K2Cz4U2iAPrxLKq4cyheMUoP4FpiYjYy5vklCAFxJlz8RcqVhwNNHH6mJ6Y2DJN9AfnGE88eVpQcLjXdNs6vUXApW-BmMRK7ZG5tduO46t3xRcDZh9UUf6RrWWA3lsznyZOZL0Ll-zxyoYWRwvuEhs15sexRRVS_Qv0og3Bo0XLLEDADL5QRlfVz7d4K1Tc0Crn8Y48STVLyLVpGW1XzeY988NUj22soZc8fHZK7Yc4aB3d6dWqn7_ncn4PIojZxSXDuGEBFTKQC7TP8-vjpgvanb5fgQRygqQ7DyYQBXrww3zJ2r-bmzCIiqTKflsI1-_vE0THhVf6nJBuWNFBJckivMqoQ9QVEeMRVt_VbnzvovKyYrnuX1NeUNYRTi7TF-lIMJJKMkk9MLMRANXBGnvpvZGEwmxXJZYRnXO_8L6eatfw1yYjdYP8Xf8Ka0njPWdUEJggWp11P8D3HpNrjCQtKlqZ68v9OZr3SnAABIE94IfnBzvr_QTPXrfHNCOlZxo13LQ6-82MpcQDYCcmwBaQf8YRvqFJmJphP-aJaIdcwcMtbbuIPffWbSvBQES8yWn59ZYV72eXSSp8w8aeIa5f_UO-XH7S4ur2hbS7qqfQEiARjKkqB5EC_Jg3asaA8lFMQ"  # your token
        driver.execute_script("""
            let textarea = document.getElementById("g-recaptcha-response");
            if (textarea) {
                textarea.style.display = 'block';
                textarea.value = arguments[0];
                textarea.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """, recaptcha_token)

        try:
            checkbox = driver.find_element(By.ID, "rememberme")
            if not checkbox.is_selected():
                checkbox.click()
        except Exception as e:
            print("Remember me checkbox issue:", e)

        wait.until(EC.element_to_be_clickable((By.NAME, "login"))).click()
        print("Login submitted")

        # Step 2: Click "Apply Now"
        try:
            apply_now_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@href, '/apply/') and contains(text(), 'Apply Now')]")))
            apply_now_btn.click()
            print("Apply Now button clicked")
        except TimeoutException:
            print("Could not find or click 'Apply Now'")
            return

        time.sleep(2)

        # Step 3: Click "Standard eVisa" link
        try:
            standard_evisa_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@href, '/product/standard-evisa/')]")))
            standard_evisa_btn.click()
            print("Standard eVisa button clicked")
        except TimeoutException:
            print("Could not find or click 'Standard eVisa' button")
            return

        # Step 1 of form
        nationality_select = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_6509b31de9a64]")))
        Select(nationality_select).select_by_value(cred['nationality'])

        passport_select = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650d6cdecc381]")))
        Select(passport_select).select_by_value(cred['passport'])

        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.wapf_btn_next"))).click()
        print("Moved to Step 2")

        # Step 2
        purpose_select = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650d6dbdb9db3]")))
        Select(purpose_select).select_by_value(cred['purpose'])

        date_input = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650df9e3e84f1]")))
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
        """, date_input, cred['date'])

        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.wapf_btn_next"))).click()
        print("Moved to Step 3")

        # Step 3
        surname_input = wait.until(EC.element_to_be_clickable((By.NAME, "wapf[field_650d768122452]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", surname_input)
        surname_input.clear()
        surname_input.send_keys(cred['surname'])

        othername_input = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650d76d1545cc]")))
        othername_input.send_keys(cred['other_name'])

        dob_input = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650d76f51313f]")))
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
        """, dob_input, cred['dob'])

        cob_select = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650d773085c3d]")))
        Select(cob_select).select_by_value(cred['cob'])

        pob_input = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650dfac3aa534]")))
        pob_input.send_keys(cred['pob'])

        sex_select = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650dfaeefa587]")))
        Select(sex_select).select_by_value(cred['sex'])

        occupation_select = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_650dfb2272ee8]")))
        Select(occupation_select).select_by_value(cred['occupation'])

        phno_input = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_651159a2ddd15]")))
        phno_input.send_keys(cred["mobileno"])

        addr_input = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_65115a1889505]")))
        addr_input.send_keys(cred["address"])

        email_input = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_65115a4dca349]")))
        email_input.send_keys(cred["email"])

        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.wapf_btn_next"))).click()
        print("Moved to Step 4")

        # Step 4 - Passport details
        passportno_input = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_651167afed118]")))
        passportno_input.send_keys(cred["passportNo"])

        pid_input = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_651168085f7e4]")))
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
        """, pid_input, cred['passportIssueDate'])

        ped_input = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_651168410fb3e]")))
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
        """, ped_input, cred['passportExpiryDate'])

        # FILE UPLOAD via Drag and Drop
        image_file_path = os.path.abspath('C:/Users/DELL/OneDrive/Desktop/sele/IRAQ3.jpg')
        dropzone = wait.until(EC.presence_of_element_located((By.ID, "wapf-dz-65116994dec8e")))

        print(f"Uploading file via drag-drop: {image_file_path}")
        drop_file(driver, dropzone, image_file_path)

        # Wait for upload preview element indicating upload success
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dz-preview")))
        print("File upload complete.")

    
        azerbaddr_input = wait.until(EC.presence_of_element_located((By.NAME, "wapf[field_65116a8a184b1]")))
        azerbaddr_input.send_keys(cred["azb_address"])

    
        checkbox = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@type='checkbox' and contains(@name, '650d75f5637e6')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        driver.execute_script("arguments[0].click();", checkbox)

        time.sleep(5)  

        # Click Final Submit button
        try:
            final_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.single_add_to_cart_button")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", final_button)
            final_button.click()
            print("Final 'Complete Application' button clicked!")
        except Exception as e:
            print(f"Error clicking final button: {e}")
            driver.execute_script("arguments[0].click();", final_button)

        input("Press Enter to exit...")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
