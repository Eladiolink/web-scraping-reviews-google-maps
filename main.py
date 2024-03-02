from selenium import webdriver
import csv, json, re, os
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
import time

load_dotenv()


def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    count = int(os.getenv("Messages"))
    divs = []
    div_sem_duplicate = []
    boolean = True
    last = 0
    countCoverge = 0
    converge = int(os.getenv("Converge"))
    while boolean:
        div = []
        time.sleep(2)  # Aguarda um tempo para a página carregar após a rolagem

        driver.execute_script("document.querySelector('.DxyBCb').scrollTo(0, 300000000000000000000000);")
        time.sleep(1)
        driver.execute_script("document.querySelectorAll('.w8nwRe').forEach(elm => elm.click())")
        div = driver.execute_script(f"return document.querySelectorAll('.jJc9Ad');")

        for i in div[len(div_sem_duplicate):]:
            res = extract_data(driver,i)
            if res != False: divs.append(res)

        div_sem_duplicate = removeDuplicate(divs)
        print(len(div_sem_duplicate))
        # div_sem_duplicate = divs
        if last == len(div_sem_duplicate):
            countCoverge+=1
        else:
            last = len(div_sem_duplicate)

        if countCoverge == converge:
            print("Break by coverge")
            break

        if len(div_sem_duplicate) >= count: break
    return div_sem_duplicate

def removeDuplicate(array_de_dicionarios):
    # Convertendo os dicionários em tuplas para torná-los hasháveis
    tuplas = [tuple(d.items()) for d in array_de_dicionarios]

    # Removendo duplicatas
    tuplas_sem_duplicatas = set(tuplas)

    # Convertendo as tuplas de volta para dicionários
    return [dict(t) for t in tuplas_sem_duplicatas]


def extract_data(driver, html_elm):
    html_list = html_elm.get_attribute('outerHTML')
    padrao = r'<span class="wiI7pd">(.*?)</span>'
    padrao2 = r'<span class="review-full-text" style="display:none">(.*?)</span>'
    nota = r'<span class="kvMYJc" role="img" aria-label="(.*?) "'
    nota2 = r'<span class="fzvQIb">(.*?)/'

    resultado = re.search(padrao, html_list)
    resultado2 = re.search(padrao2,html_list)

        # Se o padrão for encontrado, imprime o texto correspondente

    texto_extraido = ""
    if resultado:
        texto_extraido = resultado.group(1)
    elif resultado2:
        texto_extraido = resultado2.group(1)

    resultadoNota = re.search(nota,html_list)
    resultadoNota2 = re.search(nota2,html_list)

    nota = ""

    if resultadoNota:
        nota = resultadoNota.group(1)[0]
    elif resultadoNota2:
        nota = resultadoNota2.group(1)

    if nota == "": return False
    if texto_extraido == "": return False
    notaFloat = int(nota)

    return  {"Nota":notaFloat,"Comentario":texto_extraido}

def crawl(url):
    driver = webdriver.Chrome()  # Você precisará baixar o driver do Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
    driver.get(url)
    data = scroll_page(driver)
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
