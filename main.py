from selenium import webdriver
import csv, json, re, os
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
import time

load_dotenv()


def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    divs = []

    while True:
        time.sleep(2)  # Aguarda um tempo para a página carregar após a rolagem
        countToScroll = int(os.getenv("CountToScroll"))
        for i in range(1,countToScroll):
            driver.execute_script("document.querySelector('.DxyBCb').scrollTo(0, 300000000000000000000000);")
            time.sleep(2)
            driver.execute_script("document.querySelectorAll('.w8nwRe').forEach(elm => elm.click())")
            div = driver.execute_script(f"return document.querySelectorAll('.jJc9Ad');")

            for i in div:
                divs.append(i)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    div_sem_duplicate = list(set(divs))
    return div_sem_duplicate

def extract_data(driver, data):
    # Aqui você pode extrair os dados que deseja da página
    # Exemplo de extração de títulos de postagens em um site de blog:
    time.sleep(2)
    divs = driver.execute_script(f"return document.querySelectorAll('.jJc9Ad');")
    # html_list = [element.outerHTML for element in divs]

    html_list = [element.get_attribute('outerHTML') for element in data]

    # div_element = divs[0].find_element_by_css_selector("review-full-text")

    # for title in titles:
    text = []
    for i in range(0, len(html_list)):
        padrao = r'<span class="wiI7pd">(.*?)</span>'
        padrao2 = r'<span class="review-full-text" style="display:none">(.*?)</span>'
        nota = r'<span class="kvMYJc" role="img" aria-label="(.*?) "'
        resultado = re.search(padrao, html_list[i])
        texto_extraido = ""
        # Se o padrão for encontrado, imprime o texto correspondente

        if resultado:
            texto_extraido = resultado.group(1)

        resultado2 = re.search(padrao2,html_list[i])

        if resultado2:
            texto_extraido = resultado2.group(1)

        resultadoNota = re.search(nota,html_list[i])

        nota = ""
        if resultadoNota:
            nota = resultadoNota.group(1)[0]
        else:
            nota = ""

        if nota == "": continue
        notaFloat = int(nota)
        text.append({"Nota":notaFloat,"Comentario":texto_extraido})

    return text

def crawl(url):
    driver = webdriver.Chrome()  # Você precisará baixar o driver do Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
    driver.get(url)
    apt = scroll_page(driver)
    data = extract_data(driver,apt)
    driver.quit()

    return data

def export_to_csv(dados,name):
    # Nome do arquivo CSV de saída
    nome_arquivo = name+".csv"

    # Lista de chaves (campos) para assegurar que as colunas sejam escritas na ordem correta
    chaves = ["Nota", "Comentario"]

    # Escrever os dados no arquivo CSV
    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
        escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=chaves)

        # Escrever cabeçalho
        escritor_csv.writeheader()

        # Escrever os dados
        for linha in dados:
            escritor_csv.writerow(linha)

    print("Dados exportados para", nome_arquivo)

# Nome do arquivo JSON de saída
def export_to_json(dados,name):
    nome_arquivo = name+".json"

    # Escrever os dados no arquivo JSON
    with open(nome_arquivo, 'w',encoding='utf-8') as arquivo_json:
        json.dump(dados, arquivo_json,ensure_ascii=False, indent=4)

    print("Dados exportados para", nome_arquivo)

if __name__ == '__main__':
    URL = os.getenv("URL")
    NameFile = os.getenv("NameFile")
    data = crawl(URL)

    export_to_csv(data,NameFile)

    export_to_json(data,NameFile)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
