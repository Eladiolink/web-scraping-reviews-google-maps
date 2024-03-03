from selenium import webdriver
def crawl(url, scroll_page):
    """Crawls a URL and extracts data."""
    # Inicia o driver do Chrome
    driver = webdriver.Chrome()
    
    driver.get(url)
    data = scroll_page(driver)
    driver.quit()
    return data