from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from io import StringIO
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with webdriver.Chrome() as driver:
    driver.get("https://www.coingecko.com/pt")
    driver.implicitly_wait(5)

    driver.execute_script("Modal.show('currency_selector')")
    driver.find_element(By.CSS_SELECTOR, "div[data-iso-code='brl']").click()
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    botao = driver.find_element(By.CSS_SELECTOR, "div.gecko-pagination-selector button")
    driver.execute_script("arguments[0].click();", botao)

    opcao = driver.find_element(By.XPATH, "//span[contains(text(),'300')]")
    driver.execute_script("arguments[0].click();", opcao)

    dados_coletatos = []

    while True:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        tabela = driver.find_element(By.TAG_NAME, "table")
        df = pd.read_html(StringIO(tabela.get_attribute("outerHTML")),
                          thousands=".",
                          decimal=",",
                          skiprows=1)[0]

        df.columns = [
            "favorito",
            "id",
            "moeda",
            "acao",
            "preco",
            "variacao_1h",
            "variacao_24h",
            "variacao_7d",
            "variacao_30d",
            "volume_24h",
            "capitalizacao_de_mercado",
            "fdv",
            "fdv_sobre_capitalizacao",
            "grafico_variacao",
        ]

        dados_coletatos.append(df)

        try:
            driver.find_element(By.CSS_SELECTOR, "a[aria-label='next']").click()
        except:
            print(f"Encerrando a execução na página {driver.current_url}")
            break

df_final = pd.concat(dados_coletatos)
df_final.to_csv("coingecko_dados.csv", index=False)
