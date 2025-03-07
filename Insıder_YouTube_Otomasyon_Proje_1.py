import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Tarayıcıyı daha gerçekçi hale getirme seçenekleri
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Selenium otomasyonunu gizlemek için ekstra script
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    # Google'ı Aç
    driver.get("https://www.google.com")

    # Arama kutusunu bul ve "useinsider youtube" yaz
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys("useinsider youtube")
    search_box.send_keys(Keys.RETURN)

    # Sonuçların yüklenmesini bekle ve "Insider" kelimesini içeren ilk sonucu tıkla
    first_result = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h3[contains(text(), 'Insider')]"))
    )
    first_result.click()

    # Yüklenmesini bekle ve başlıkta doğrulama yap
    WebDriverWait(driver, 10).until(EC.title_contains("Insider - YouTube"))
    assert "Insider - YouTube" in driver.title

    print("------------------------------------------")
    print("Automation ended at:", datetime.datetime.now())

finally:
    # Tarayıcıyı kapatmadan önce bekleyip kapat
    time.sleep(3)
    driver.quit()

