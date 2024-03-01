from selenium import webdriver
import csv, json, re

from selenium.webdriver.common.keys import Keys
import time

def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        time.sleep(2)  # Aguarda um tempo para a página carregar após a rolagem
        # document.querySelector('.review-dialog-list').scrollTo(0, 3000000000000)
        for i in range(1,2):
            driver.execute_script("document.querySelector('.review-dialog-list').scrollTo(0, 3000000000000);")
            time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_data(driver):
    # Aqui você pode extrair os dados que deseja da página
    # Exemplo de extração de títulos de postagens em um site de blog:
    time.sleep(2)
    # titles = driver.find_elements_by_xpath("//div[@class='gws-localreviews__google-review']")
    divs = driver.execute_script(f"return document.querySelectorAll('.gws-localreviews__google-review');")
    # html_list = [element.outerHTML for element in divs]
    html_list = [element.get_attribute('outerHTML') for element in divs]

    # div_element = divs[0].find_element_by_css_selector("review-full-text")

    # for title in titles:
    print(html_list[0])
    text = []
    for i in range(0, len(html_list)):
        padrao = r'<span data-expandable-section="" tabindex="-1">(.*?)</span>'
        padrao2 = r'<span class="review-full-text" style="display:none">(.*?)</span>'
        nota = r'<span class="lTi8oc z3HNkc" aria-label="Classificado como (.*?) de 5," role="img">'
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
            nota = resultadoNota.group(1)
        else:
            nota = ""
        notaFloat = float(nota.replace(",","."))
        text.append({"Nota":notaFloat,"Comentario":texto_extraido})

    return text

def crawl(url):
    driver = webdriver.Chrome()  # Você precisará baixar o driver do Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
    driver.get(url)
    scroll_page(driver)
    data = extract_data(driver)
    driver.quit()

    return data

def export_to_csv(dados):
    # Nome do arquivo CSV de saída
    nome_arquivo = "dados.csv"

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
def export_to_json(dados):
    nome_arquivo = "dados.json"

    # Escrever os dados no arquivo JSON
    with open(nome_arquivo, 'w') as arquivo_json:
        json.dump(dados, arquivo_json)

    print("Dados exportados para", nome_arquivo)

if __name__ == '__main__':
    data = crawl("https://www.google.com/search?q=Shooping+Salgueiro&sca_esv=59998079312419c0&sxsrf=ACQVn09ZYoLhj5tjZOtPjaQi570GOvb4bw%3A1709254995806&ei=UynhZeHhMLDY1sQPpYOM-Ak&udm=&ved=0ahUKEwih1-uG79GEAxUwrJUCHaUBA58Q4dUDCBE&uact=5&oq=Shooping+Salgueiro&gs_lp=Egxnd3Mtd2l6LXNlcnAiElNob29waW5nIFNhbGd1ZWlybzIQEC4YgAQYDRjHARivARiOBTIHEAAYgAQYDTIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIKEAAYFhgeGA8YCjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIIEAAYBRgeGA0yHxAuGIAEGA0YxwEYrwEYjgUYlwUY3AQY3gQY4ATYAQJI8j5Q3ApYlz1wAngBkAEEmAG4AqAB2yaqAQgwLjE4LjcuMbgBA8gBAPgBAZgCFaAC8iCoAhTCAgoQABhHGNYEGLADwgINEAAYgAQYigUYQxiwA8ICChAjGIAEGIoFGCfCAggQABiABBiSA8ICBRAAGIAEwgIIEAAYgAQYsQPCAgcQIxjqAhgnwgITEAAYgAQYigUYQxjqAhi0AtgBAcICCxAuGIMBGLEDGIAEwgILEC4YgAQYsQMYgwHCAhEQLhiABBixAxiDARjHARjRA8ICBRAuGIAEwgILEAAYgAQYsQMYgwHCAgQQIxgnwgIQEAAYgAQYigUYQxixAxiDAcICCxAuGIAEGMcBGK8BwgIWEC4YgAQYigUYQxixAxiDARjHARjRA8ICDhAuGIAEGLEDGMcBGK8BwgINEC4YgAQYxwEY0QMYCsICChAAGIAEGIoFGEPCAg0QABiABBixAxiDARgKwgIOEC4YgAQYigUYsQMYgwHCAg4QLhiABBixAxiDARjUAsICHBAuGIAEGMcBGNEDGAoYlwUY3AQY3gQY4ATYAQLCAhYQLhhDGIMBGMcBGLEDGNEDGIAEGIoFwgINEAAYgAQYChixAxiDAcICChAAGIAEGAoYsQPCAg0QABiABBiKBRhDGLEDwgIlEC4YQxiDARjHARixAxjRAxiABBiKBRiXBRjcBBjeBBjgBNgBAsICEBAuGIAEGAoYsQMYxwEYrwHCAgsQABiABBiKBRiSA8ICEBAuGIAEGAoYkgMYxwEYrwHCAhAQABiABBiKBRhDGLEDGMkDwgINEC4YgAQYChjHARivAcICHxAuGIAEGAoYsQMYxwEYrwEYlwUY3AQY3gQY4ATYAQLCAgcQABiABBgKwgIQEC4YgAQYChjHARivARiOBcICBhAAGAMYCsICHxAuGIAEGAoYxwEYrwEYjgUYlwUY3AQY3gQY4ATYAQLCAhAQLhgKGK8BGMcBGIAEGI4FwgIfEC4YChivARjHARiABBiOBRiXBRjcBBjeBBjgBNgBAsICDRAuGA0YrwEYxwEYgATCAggQABgWGB4YCsICCBAAGBYYHhgPmAMXiAYBkAYKugYGCAEQARgBugYGCAIQARgUkgcIMi41LjEzLjE&sclient=gws-wiz-serp#lrd=0x7a0918fe0694c13:0x40f861404fa6ca00,1,,,,")
    export_to_csv(data)
    export_to_json(data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
