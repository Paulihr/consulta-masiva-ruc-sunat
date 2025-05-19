from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time

# 1. Lee lista de RUC desde Excel
df_ruc = pd.read_excel(
    r'C:\Users\pauli\OneDrive\Escritorio\ruc_list.xlsx',  # Ruta a tu archivo Excel
    sheet_name='RUCs'                                      # Hoja donde están los RUC
)
ruc_list = df_ruc['RUC'].astype(str).tolist()             # Convierte a lista de strings

# 2. Prepara WebDriver
edge_options = Options()
# edge_options.add_argument('--headless')  # Puedes activar modo headless si lo deseas
service = Service(executable_path=r'C:\Users\pauli\Downloads\msedgedriver.exe')
driver = webdriver.Edge(service=service, options=edge_options)
wait = WebDriverWait(driver, 10)

# 3. Prepara la colección de resultados
results = []

# 4. Abre la página de consulta RUC una sola vez
driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp')
input_ruc = driver.find_element(By.XPATH, '//input[@placeholder="Ingrese RUC"]')
btn_buscar = driver.find_element(By.ID, 'btnAceptar')

# 5. Itera por cada RUC
for ruc_busqueda in ruc_list:
    try:
        # 5.1 Ingresa el RUC y envía la consulta
        input_ruc.clear()
        input_ruc.send_keys(ruc_busqueda)
        btn_buscar.click()

        # 5.2 Espera que aparezca el bloque con "Número de RUC:"
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//h4[contains(text(), 'Número de RUC:')]")
        ))

        # 5.3 Extrae y divide el número de RUC y el nombre
        ruc_text_el = driver.find_element(
            By.XPATH,
            "//div[contains(@class, 'list-group-item')]/div/div[h4[contains(text(), 'Número de RUC:')]]"
            "/following-sibling::div/h4"
        )
        numero_ruc, nombre = ruc_text_el.text.split(' - ', 1)
        detalle = {
            'Número de RUC': numero_ruc.strip(),
            'Nombre': nombre.strip()
        }

        # 5.4 Mapeo de los demás campos a extraer
        mapeo = {
            "Nombre Comercial": "//h4[contains(text(), 'Nombre Comercial')]/../following-sibling::div/p",
            "Tipo Contribuyente": "//h4[contains(text(), 'Tipo Contribuyente')]/../following-sibling::div/p",
            "Estado del Contribuyente": "//h4[contains(text(), 'Estado del Contribuyente')]/../following-sibling::div/p",
            "Condición del Contribuyente": "//h4[contains(text(), 'Condición del Contribuyente')]/../following-sibling::div/p",
            "Domicilio Fiscal": "//h4[contains(text(), 'Domicilio Fiscal')]/../following-sibling::div/p"
        }

        # 5.5 Itera sobre cada campo y lo añade al diccionario
        for campo, xpath in mapeo.items():
            try:
                detalle[campo] = wait.until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                ).text.strip()
            except (TimeoutException, NoSuchElementException):
                detalle[campo] = None

        # 5.6 Agrega el diccionario de este RUC a la lista de resultados
        results.append(detalle)

        # 5.7 Vuelve a la página inicial para la siguiente consulta
        driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp')
        input_ruc = driver.find_element(By.XPATH, '//input[@placeholder="Ingrese RUC"]')
        btn_buscar = driver.find_element(By.ID, 'btnAceptar')
        time.sleep(1)  # pequeña pausa para no sobrecargar

    except Exception as e:
        print(f"Error con RUC {ruc_busqueda}: {e}")
        # Aquí podrías registrar el error en un log si lo deseas

# 6. Cierra el navegador
driver.quit()

# 7. Guarda todos los resultados en un Excel
df_result = pd.DataFrame(results)
df_result.to_excel(r'C:\Users\pauli\OneDrive\Escritorio\Estadohabido_varios.xlsx', index=False)

print("Proceso completado. Revisa 'Estadohabido_varios.xlsx' en tu escritorio.")
