from dataclasses import dataclass
from selenium import webdriver 
from selenium.webdriver.common.by import By

@dataclass
class Configs:
    url:str = "https://www.amazon.co.jp/ref=nav_logo"
    word:str = "フットサルシューズ"
    search_tag : tuple = (By.ID, "twotabsearchtextbox")
    searchbox_tag : tuple  = (By.ID, "nav-search-submit-button")
    max_page :int = 3
    get_url_tag : tuple  = (By.CSS_SELECTOR,"a.a-link-normal.s-no-outline")
    next_btn_tag : tuple  = (By.CSS_SELECTOR,".s-pagination-item.s-pagination-next")
    title_tag : tuple  = (By.ID, "productTitle")
    price_tag  : tuple = (By.CSS_SELECTOR,"span.a-price-whole")   
    asin_tag : tuple  = (By.XPATH, "//span[contains(text(), 'ASIN')]//following-sibling::span")