from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dataclasses import dataclass
from dataclasses import asdict
import json

driver = webdriver.Chrome()
driver.get("https://curso-web-scraping.pages.dev/#/desafio/4")

@dataclass
class Produto:
  titulo: str
  e_frete_gratis: bool
  e_parcelamento_sem_juros: bool
  e_envio_internacional: bool
  esta_em_oferta: bool
  numero_estrelas: int
  descricao: str
  foto: str # link da imagem, por isso string
  preco: int

wait = WebDriverWait(driver=driver, timeout=10, poll_frequency=1)

actions = ActionChains(driver)

def acessar_produtos(categoria: str):
  driver.get("https://curso-web-scraping.pages.dev/#/desafio/4")
  (
    ActionChains(driver)
    .click(driver.find_element(By.XPATH, f"//h1[contains(text(), '{categoria}')]"))
    .perform()
  )

def capturar_dados_do_produtos():
  dados = []

  while True:
    wait.until(EC.visibility_of_all_elements_located(locator=(By.CSS_SELECTOR, "form#filtros + div div > img")))

    produtos = driver.find_elements(By.CSS_SELECTOR, "form#filtros + div div:has(>img)")

    for produto in produtos:
      dados_do_produto = Produto(
        titulo= produto.find_element(By.TAG_NAME, "h5").text,
        e_frete_gratis= True if produto.find_elements(By.CSS_SELECTOR, "div.bg-blue-100") else False,
        e_parcelamento_sem_juros= True if produto.find_elements(By.CSS_SELECTOR, "div.bg-green-100") else False,
        e_envio_internacional= True if produto.find_elements(By.CSS_SELECTOR, "div.bg-orange-100") else False,
        esta_em_oferta= True if produto.find_elements(By.CSS_SELECTOR, "div.bg-purple-100") else False,
        numero_estrelas= len(produto.find_elements(By.CSS_SELECTOR, "svg.text-yellow-300")),
        descricao= produto.find_element(By.TAG_NAME, "p").text,
        foto= produto.find_element(By.TAG_NAME, "img").get_attribute("src"),
        preco = produto.find_element(By.CSS_SELECTOR, "div:has(>span:nth-last-child(2)) > span:nth-child(2)").text
      )

      dados.append(dados_do_produto)

    proximo = driver.find_element(By.CSS_SELECTOR, "form#filtros + div button:last-child")

    try:
      proximo.click()
    except:
      break

  return dados

def preencher_filtros(
    frete_gratis = bool,
    parcelamento_sem_juros = bool,
    envio_internacional = bool, 
    em_oferta = bool,
    preco_minimo = int, 
    preco_maximo = int, 
    nota = int,  
):
  # Filtros
  frete = driver.find_element(By.ID, "frete")
  parcelamento = driver.find_element(By.ID, "parcelamento")
  internacional = driver.find_element(By.ID, "envio-internacional")
  oferta = driver.find_element(By.ID, "oferta")

  # Preços
  preco_de = driver.find_element(By.ID, "price-from")
  preco_ate = driver.find_element(By.ID, "price-to")

  # Notas
  nota5 = driver.find_element(By.ID, "five-stars")
  nota4 = driver.find_element(By.ID, "four-stars")
  nota3 = driver.find_element(By.ID, "three-stars")
  nota2 = driver.find_element(By.ID, "two-stars")
  nota1 = driver.find_element(By.ID, "one-star")

  # Ações
  enviar = driver.find_element(By.CSS_SELECTOR, "form#filtros button[type='submit']")
  limpar = driver.find_element(By.CSS_SELECTOR, "form#filtros button[type='reset']")

  actions.send_keys_to_element(preco_de, preco_minimo)
  actions.send_keys_to_element(preco_ate, preco_maximo)

  if frete_gratis:
    actions.click(frete)

  if parcelamento_sem_juros:
    actions.click(parcelamento)

  if envio_internacional:
    actions.click(internacional)

  if em_oferta:
    actions.click(oferta)

  # Limpar
  actions.key_down(Keys.CONTROL)
  actions.send_keys_to_element(preco_de, "a")
  actions.key_up(Keys.CONTROL)
  actions.send_keys_to_element(preco_de, Keys.DELETE)

  actions.key_down(Keys.CONTROL)
  actions.send_keys_to_element(preco_ate, "a")
  actions.key_up(Keys.CONTROL)
  actions.send_keys_to_element(preco_ate, Keys.DELETE)

  actions.send_keys_to_element(preco_de, preco_minimo)
  actions.send_keys_to_element(preco_ate, preco_maximo)

  match nota:
    case 5:
      actions.click(nota5)
    case 4:
      actions.click(nota4)
    case 3:
      actions.click(nota3)
    case 2:
      actions.click(nota2)
    case 1:
      actions.click(nota1)

  actions.click(enviar)
  actions.perform()

# Selecionar todos os produtos da categoria Celulares com frete grátis, em oferta, preço entre R$500 e R$2500 reais e com 4 estrelas.

acessar_produtos(categoria="Celulares")

preencher_filtros(
  frete_gratis = True,
  parcelamento_sem_juros = False,
  envio_internacional = False, 
  em_oferta = True,
  preco_minimo = 500, 
  preco_maximo = 2500, 
  nota = 4,  
)

celulares = capturar_dados_do_produtos()

# Selecionar todos os produtos da categoria TVs com envio internacional, preço até R$5000 e 5 estrelas.

acessar_produtos(categoria="TVs")

preencher_filtros(
  frete_gratis = False,
  parcelamento_sem_juros = False,
  envio_internacional = True, 
  em_oferta = False,
  preco_minimo = 1, 
  preco_maximo = 5000, 
  nota = 5,  
)

tvs = capturar_dados_do_produtos()

# Selecionar todos os produtos da categoria Games com parcelamento sem juros, frete grátis, preço entre R$2000 e R$8000 reais e 3 estrelas.

acessar_produtos(categoria="Games")

preencher_filtros(
  frete_gratis = True,
  parcelamento_sem_juros = True,
  envio_internacional = False, 
  em_oferta = False,
  preco_minimo = 2000, 
  preco_maximo = 8000, 
  nota = 3,  
)

games = capturar_dados_do_produtos()

# Selecionar todos os produtos da categoria Notebooks com parcelamento sem juros, em oferta, preço entre R$1234 e R$7896 reais e 3 estrelas.

acessar_produtos(categoria="Notebooks")

preencher_filtros(
  frete_gratis = False,
  parcelamento_sem_juros = True,
  envio_internacional = False, 
  em_oferta = True,
  preco_minimo = 1234, 
  preco_maximo = 7896, 
  nota = 3,  
)

notebooks = capturar_dados_do_produtos()

# Exportar todos os dados coletados para um json e um CSV

todos_os_produtos = celulares + tvs + games + notebooks

with open("desafio_4.json", "w") as file:
  data_formatted = [asdict(d) for d in todos_os_produtos]
  json.dump(data_formatted, file, ensure_ascii=False)