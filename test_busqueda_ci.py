from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.binary_location = "/opt/chrome114/chrome"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

try:
    print("🌐 Navegando a DuckDuckGo...")
    driver.get("https://duckduckgo.com/")
    
    # Esperar a que la página se cargue completamente
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    print("✅ Página cargada correctamente")
    
    # Realizar búsqueda
    print("🔍 Realizando búsqueda...")
    buscador = driver.find_element(By.NAME, "q")
    buscador.send_keys("inmuebles en Bogotá")
    buscador.send_keys(Keys.RETURN)
    
    # Esperar resultados con múltiples selectores posibles
    print("⏳ Esperando resultados...")
    
    # Intentar diferentes selectores
    selectores_posibles = [
        'article[data-testid="result"]',
        'div[data-testid="result"]',
        '[data-testid="result"]',
        '.result',
        '.web-result',
        '.result__body'
    ]
    
    resultados = []
    for selector in selectores_posibles:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
            )
            resultados = driver.find_elements(By.CSS_SELECTOR, selector)
            if len(resultados) > 0:
                print(f"✅ Encontrados {len(resultados)} resultados con selector: {selector}")
                break
        except:
            continue
    
    # Si no encontró resultados con los selectores específicos, buscar cualquier elemento que contenga texto de resultados
    if len(resultados) == 0:
        print("🔄 Intentando buscar resultados de forma más general...")
        time.sleep(3)  # Esperar un poco más
        
        # Buscar elementos que contengan enlaces o texto de resultados
        resultados = driver.find_elements(By.CSS_SELECTOR, 'a[href*="http"]')
        resultados = [r for r in resultados if r.text.strip() and len(r.text.strip()) > 10]
    
    assert len(resultados) > 0, f"No se encontraron resultados. URL actual: {driver.current_url}"
    
    print(f"✅ Prueba funcional CI completada con éxito - {len(resultados)} resultados encontrados")
    
    # Opcional: mostrar algunos resultados para debug
    for i, resultado in enumerate(resultados[:3]):
        try:
            texto = resultado.text.strip()[:100]
            if texto:
                print(f"Resultado {i+1}: {texto}...")
        except:
            pass

except Exception as e:
    print(f"❌ Error: {e}")
    print(f"URL actual: {driver.current_url}")
    
    # Tomar screenshot para debug
    try:
        driver.save_screenshot("failure.png")
        print("📸 Screenshot guardado como failure.png")
    except:
        pass
    
    # Mostrar el HTML de la página para debug
    try:
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📄 HTML de la página guardado como page_source.html")
    except:
        pass
    
    raise

finally:
    driver.quit()