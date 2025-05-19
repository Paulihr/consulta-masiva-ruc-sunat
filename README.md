# 🕵️‍♂️ Web Scraping de RUC desde SUNAT con Selenium

Este proyecto automatiza la consulta de múltiples RUCs en el portal SUNAT utilizando Python y Selenium. Extrae información clave como razón social, estado, condición del contribuyente, domicilio fiscal, entre otros, y exporta los resultados a Excel.

## 📦 Requisitos

1. **Python 3.10 o superior**
2. **Librerías necesarias**  
   Abre la terminal (CMD, PowerShell o VSCode Terminal) y ejecuta:

   ```bash
   pip install selenium pandas openpyxl

### 🔧 Configuración del WebDriver (Edge)

Este script utiliza Microsoft Edge WebDriver.  
Cada usuario debe descargar la versión compatible con su propio navegador Edge:

1. Ve a [descargar WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
2. Verifica tu versión de Microsoft Edge:
   - Abre Edge > haz clic en los 3 puntos (arriba a la derecha) > "Ayuda y comentarios" > "Acerca de Microsoft Edge"
3. Descarga el WebDriver que **coincida exactamente con la versión de tu navegador**
4. Extrae el archivo `msedgedriver.exe` en una ruta fácil de encontrar
5. En el código, ajusta esta línea con tu ruta:

```python
service = Service(executable_path=r'C:\ruta\msedgedriver.exe')

### ⚙️ Configuración previa

Antes de ejecutar el script, realiza los siguientes pasos de configuración:

1. **Cambia la ruta del archivo Excel** donde tienes los RUCs:

   ```python
   df_ruc = pd.read_excel(r'C:\Users\tu_usuario\OneDrive\Escritorio\ruc_list.xlsx')
   ```

2. **Cambia la ruta del WebDriver de Microsoft Edge**:

   ```python
   service = Service(executable_path=r'C:\Users\tu_usuario\Downloads\msedgedriver.exe')
   ```

3. **Asegúrate de que tu archivo Excel tenga una columna llamada `"RUC"`**.

> 💡 **Nota:** No necesitas crear el archivo `Estadohabido_varios.xlsx` manualmente. El script lo generará automáticamente al finalizar la ejecución, con toda la información extraída.

---

### 🚀 Ejecución

Ejecuta el script con el siguiente comando en la terminal:

```bash
python scrape_sunat.py
```

- El navegador se abrirá automáticamente y procesará cada RUC uno por uno.
- Al finalizar, se generará un archivo llamado `Estadohabido_varios.xlsx` con los resultados.

---

### 📤 ¿Qué información se obtiene?

Por cada RUC consultado, se extrae la siguiente información desde SUNAT:

- Número de RUC  
- Nombre o Razón Social  
- Nombre Comercial  
- Tipo de Contribuyente  
- Estado del Contribuyente  
- Condición del Contribuyente  
- Domicilio Fiscal
