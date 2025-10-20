import datetime
import json
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import Select


driver = webdriver.Chrome()
driver.get("https://curso-web-scraping.pages.dev/#/desafio/1")


with open("./desafio_1.json") as file:
  data = json.load(file)

for item in data:
  email = driver.find_element(By.NAME, "email")
  senha = driver.find_element(By.NAME, "senha")

  email.clear()
  senha.clear()

  email.send_keys(item["email"])
  senha.send_keys(item["senha"])

  dt = datetime.datetime.strptime(item["data-de-nascimento"], "%Y-%m-%d")
  
  dia = Select(driver.find_element(By.NAME, "dia"))
  mes = Select(driver.find_element(By.NAME, "mes"))
  ano = Select(driver.find_element(By.NAME, "ano"))

  dia.select_by_visible_text(str(dt.day))
  mes.select_by_visible_text(str(dt.month))
  ano.select_by_visible_text(str(dt.year))

  newsletter = driver.find_element(By.ID, "airplane-mode")
  switch_on = True if newsletter.get_attribute("aria-checked") == "true" else False

  if switch_on != item["newsletter"]:
    newsletter.click()
  
  email.submit()