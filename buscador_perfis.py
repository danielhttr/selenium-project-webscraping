from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from dataclasses import dataclass
from dataclasses import asdict
import csv
from dataclasses import fields

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://curso-web-scraping.pages.dev/#/desafio/2")

with open("./desafio_2.json") as file:
    usuarios = json.load(file)

@dataclass
class Usuario:
    foto: str
    nome: str
    profissao: str
    email: str
    telefone: str
    perfil: str
    estado: str

inp = driver.find_element(By.CSS_SELECTOR, "main input[type='text']")
botao = driver.find_element(By.CSS_SELECTOR, "main button")

data = []

for usuario in usuarios:
    # Preencher o campo de busca
    inp.clear()
    inp.send_keys(usuario)

    # Esperar o botão estar clicável
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable(botao))
    botao.click()

    # Esperar resultados
    locator = (By.CSS_SELECTOR, "div.users-list > div > img")
    wait.until(EC.visibility_of_all_elements_located(locator))

    # Pega todos os usuários da lista
    users = driver.find_elements(By.CSS_SELECTOR, "div.users-list > div")

    for user in users:
        foto = user.find_element(By.TAG_NAME, "img")
        nome = user.find_element(By.TAG_NAME, "h3")
        profissao = user.find_element(By.TAG_NAME, "span")
        email = user.find_element(By.CSS_SELECTOR, "ul > li:nth-child(1)")
        telefone = user.find_element(By.CSS_SELECTOR, "ul > li:nth-child(2)")
        perfil = user.find_element(By.CSS_SELECTOR, "ul > li:nth-child(3)")
        estado = user.find_element(By.CSS_SELECTOR, "ul > li:nth-child(4)")

        dados_do_usuario = Usuario(
            foto=foto.get_attribute("src"),
            nome=nome.text,
            profissao=profissao.text,
            email=email.text[8:],
            telefone=telefone.text[10:],
            perfil=perfil.text[9:], 
            estado=estado.text[8:]
        )

        data.append(dados_do_usuario)
        
with open('dados_capturados.json', 'w') as file:
    data_formatted = [asdict(d) for d in data]
    json.dump(data_formatted, file)

with open('dados_capturados.csv', 'w') as csvfile:
    headers = [field.name for field in fields(Usuario)]
    file = csv.DictWriter(csvfile, fieldnames=headers)

    file.writeheader()

    data_formatted = [asdict(d) for d in data]
    file.writerows(data_formatted)
