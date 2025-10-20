from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass

driver = webdriver.Chrome()

@dataclass
class Usuario:
  foto: str
  nome: str
  profissao: str
  email: str
  telefone: str
  perfil: str
  estado: str


driver.switch_to.window(driver.window_handles[0])
driver.get("https://curso-web-scraping.pages.dev/#/desafio/2")
driver.implicitly_wait(time_to_wait=10)

driver.switch_to.new_window("tab")
driver.get("https://curso-web-scraping.pages.dev/#/desafio/3")
windows = {
  "busca": driver.window_handles[0],
  "cadastro": driver.window_handles[1],
}

while True:
  # Garante que estamos na tela de cadastro
  driver.switch_to.window(window_name=windows["cadastro"])
  try:
    # Obter o usuário a ser cadastrado
    usuario_busca = driver.find_element(By.ID, "usuario").text
  except:
      # Interromper a execução quando não houver mais usuário
      break
  
  # Ir para a aba com os dados de busca
  driver.switch_to.window(window_name=windows["busca"])

  # Pesquisar e obter os dados do usuário buscado
  data = []

  # Preenche as informações para pesquisa
  inp = driver.find_element(By.CSS_SELECTOR, "main input")
  inp.clear()
  inp.send_keys(usuario_busca)

  # Aguarda o botão ser clicável e faz a busca
  botao = driver.find_element(By.CSS_SELECTOR, "main button")
  wait = WebDriverWait(driver=driver, timeout=15, poll_frequency=1)
  wait.until(EC.element_to_be_clickable(mark=botao))
  botao.click()

  # Obtém todos os usuários encontrados na busca
  wait.until(EC.visibility_of_all_elements_located(locator=(By.CSS_SELECTOR, "div.users-list > div > img")))
  users = driver.find_elements(By.CSS_SELECTOR, "div.users-list > div")

  # Obtém os dados de cada usuário

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

  # Ir para a aba de cadastro
  driver.switch_to.window(window_name=windows["cadastro"])

  nome_cadastro = driver.find_element(By.NAME, "nome")
  profissao_cadastro = driver.find_element(By.NAME, "profissao")
  email_cadastro = driver.find_element(By.NAME, "email")
  telefone_cadastro = driver.find_element(By.NAME, "telefone")
  perfil_cadastro = driver.find_element(By.NAME, "usuario")
  estado_cadastro = Select(driver.find_element(By.NAME, "estado"))

  # Preencher cada um dos usuários encontrados na busca
  for dt in data:
      nome_cadastro.clear()
      profissao_cadastro.clear()
      email_cadastro.clear()
      telefone_cadastro.clear()
      perfil_cadastro.clear()

      nome_cadastro.send_keys(dt.nome)
      profissao_cadastro.send_keys(dt.profissao)
      email_cadastro.send_keys(dt.email)
      telefone_cadastro.send_keys(dt.telefone)
      perfil_cadastro.send_keys(dt.perfil)
      estado_cadastro.select_by_visible_text(dt.estado)

      nome_cadastro.submit()
