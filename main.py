import time,os
from dotenv import load_dotenv
from crawler import crawl
from data_export import export_to_csv, export_to_json
from data_manipulation import extract_data, remove_duplicate
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém as variáveis de ambiente
URL = os.getenv("URL")
NAME_FILE = os.getenv("NameFile")
MESSAGES = int(os.getenv("Messages"))
CONVERGE = int(os.getenv("Converge"))
TIMER = int(os.getenv("Timer"))

def scroll_page(driver):
    """Scrolls the page and extracts data until a condition is met."""
    divs = []
    div_sem_duplicate = []
    last = 0
    countCoverge = 0
    while True:
        time.sleep(TIMER)  # Espera a página carregar após rolar
        driver.execute_script("document.querySelector('.DxyBCb').scrollTo(0, 300000000000000000000000);")
        time.sleep(1)
        # Clica em todos os elementos '.w8nwRe'
        driver.execute_script("document.querySelectorAll('.w8nwRe').forEach(elm => elm.click())")
        # Obtém todos os elementos '.jJc9Ad'
        div = driver.execute_script("return document.querySelectorAll('.jJc9Ad');")

        # Extrai os dados dos novos elementos
        for i in div[len(div_sem_duplicate):]:
            res = extract_data(driver, i)
            if res: divs.append(res)

        # Remove duplicatas
        div_sem_duplicate = remove_duplicate(divs)
        if last == len(div_sem_duplicate):
            countCoverge += 1
        else:
            last = len(div_sem_duplicate)

        if countCoverge == CONVERGE:
            print("Break by coverge")
            break

        # Verifica se atingiu o número de mensagens desejado
        if len(div_sem_duplicate) >= MESSAGES: break
    return div_sem_duplicate

if __name__ == '__main__':
    # Inicia o processo de extração de dados
    data = crawl(URL, scroll_page)
    # Exporta os dados para CSV e JSON
    export_to_csv(data, NAME_FILE)
    export_to_json(data, NAME_FILE)