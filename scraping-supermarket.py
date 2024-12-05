from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


def get_driver():
    # Configurar Selenium en modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    # Inicializar el driver en modo headless
    return webdriver.Chrome(options=chrome_options)


@app.route('/producto', methods=['POST'])
def producto():
    data = request.get_json()
    url = data.get('url')
    driver = get_driver()
    try:
        # Navegar a la página
        driver.get(url)

        # Esperar a que los productos se carguen
        driver.implicitly_wait(10)

        # Extraer el HTML de la página
        html = driver.page_source
        print (html)
        
        # Extraer los productos con Selenium
        products = driver.find_elements(By.CLASS_NAME, "product-card")
        print (f"Found {len(products)} products with Selenium")
        driver.quit()

        # Extraer los productos con BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        products = soup.find_all("div", class_="product-card")

        print (f"Found {len(products)} products with BeautifulSoup")
        
        # Enviar los productos como JSON
        productos = []
        
        for product in products:
            name = product.find("a", class_="product-card-name").text
            price = product.find("span", class_="prices-main-price").text
            productos.append(f"{name} {price}")
            print(name, price)
            
        return jsonify(productos)
    except Exception as e:
        print(e)
        return jsonify({"message": "Error"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)