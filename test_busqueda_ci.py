from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Opciones para entorno CI (GitHub Actions)
options = Options()
options.add_argument('--headless')  # Sin interfaz gráfica
options.add_argument('--no-sandbox')  # Para contenedores
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--user-data-dir=/tmp/chrome-data')  # Evita conflicto de sesión

driver = webdriver.Chrome(options=options)

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
driver.quit()
