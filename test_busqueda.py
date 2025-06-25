from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://duckduckgo.com/")

buscador = driver.find_element(By.NAME, "q")
buscador.send_keys("inmuebles en Bogotá")
buscador.send_keys(Keys.RETURN)

# Esperar hasta que aparezcan los resultados
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article[data-testid="result"]'))
)

# Obtener los artículos
resultados = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="result"]')
assert len(resultados) > 0, "No se encontraron resultados."

print("✅ Prueba funcional completada con éxito")
driver.quit()
