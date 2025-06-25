from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.binary_location = "/opt/chrome114/chrome"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://duckduckgo.com/")
    buscador = driver.find_element(By.NAME, "q")
    buscador.send_keys("inmuebles en Bogotá")
    buscador.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article[data-testid="result"]'))
    )

    resultados = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="result"]')
    assert len(resultados) > 0, "No se encontraron resultados."

    print("✅ Prueba funcional CI completada con éxito")

except Exception as e:
    print(f"❌ Error: {e}")
    driver.save_screenshot("failure.png")
    raise

finally:
    driver.quit()
