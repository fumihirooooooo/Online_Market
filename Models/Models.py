from dataclasses import dataclass

@dataclass
class AmazonModel:
    url:str
    word:str
    search_tag:str
    searchbox_tag:str
    max_page:int
    innerheight:str
    scrollheight:str
    get_url_tag:str
    next_btn_tag:str
    title_tag: str
    price_tag:str
    asin_tag:str