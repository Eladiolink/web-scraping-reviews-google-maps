import re

def remove_duplicate(array_de_dicionarios):
    """Removes duplicates from a list of dictionaries."""
    tuplas = [tuple(d.items()) for d in array_de_dicionarios]
    tuplas_sem_duplicatas = set(tuplas)
    return [dict(t) for t in tuplas_sem_duplicatas]

def extract_data(driver, html_elm):
    """Extracts data from a HTML element."""
    html_list = html_elm.get_attribute('outerHTML')
    padrao = r'<span class="wiI7pd">(.*?)</span>'
    padrao2 = r'<span class="review-full-text" style="display:none">(.*?)</span>'
    nota = r'<span class="kvMYJc" role="img" aria-label="(.*?) "'
    nota2 = r'<span class="fzvQIb">(.*?)/'
    resultado = re.search(padrao, html_list)
    resultado2 = re.search(padrao2, html_list)
    texto_extraido = resultado.group(1) if resultado else resultado2.group(1) if resultado2 else ""
    resultadoNota = re.search(nota, html_list)
    resultadoNota2 = re.search(nota2, html_list)
    nota = resultadoNota.group(1)[0] if resultadoNota else resultadoNota2.group(1) if resultadoNota2 else ""
    if not nota or not texto_extraido: return False
    notaFloat = int(nota)
    return {"Nota": notaFloat, "Comentario": texto_extraido}