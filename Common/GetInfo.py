from Models.Models import GetInfoModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep


class GetInfo:
    def __init__(self, data: GetInfoModel):
        self.data = data

    def get_info_data(self):
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            data_samples = self.scrape_data(driver)
            return data_samples
        finally:
            driver.quit()  # 必ずリソースを解放

    def scrape_data(self, driver):
        driver.get(self.data.url)
        sleep(2)
        wait = WebDriverWait(driver, timeout=60)

        driver.find_element(*self.data.search_tag).send_keys(self.data.word)
        sleep(1)
        driver.find_element(*self.data.searchbox_tag).click()

        HREFS = self.scroll_and_collect_urls(driver, wait)
        data_samples = self.collect_item_details(driver, HREFS)

        return data_samples

    def scroll_and_collect_urls(self, driver, wait):
        HREFS = []
        page_count = 0
        
        while page_count < self.data.max_page:   #ページカウント2未満でループ処理
        #待機処理
            wait.until(EC.presence_of_element_located(self.data.get_url_tag))
            #ブラウザのウィンドウ高を取得
            win_height = driver.execute_script("return window.innerHeight")
        
            #スクロール開始一の初期値
            last_top = 1
            
            #ページ最下部までスクロール（無限ループ）
            while True:
                #スクロール前のページ高さを取得
                last_height = driver.execute_script("return document.body.scrollHeight")
                
                #スクロール開始位置を設定
                top = last_top
                
                #ページ最下部まで徐々にスクロールする処理
                while top < last_height:
                    top += int(win_height * 0.8)
                    driver.execute_script(f"window.scrollTo(0, %d)" % top)
                    sleep(0.5)

                #1秒後スクロール後のページの高さを取得
                sleep(1)
                new_last_height = driver.execute_script("return document.body.scrollHeight")
                
                #スクロール前とスクロール後のページ高さを比較
                if last_height == new_last_height:
                    break
                
                #スクロール前のページ高さを更新
                last_top = new_last_height

                #商品URLの取得
            URLS = driver.find_elements(*self.data.get_url_tag)

                #取得したURL情報をHREFSリストへ追加
            for URL in URLS:
                URL = URL.get_attribute("href")
                print("[INFO] URL :", URL)
                HREFS.append(URL)       
                
                #次のページへ
            try:
                next_btn = driver.find_element(*self.data.next_btn_tag)
                next_btn.click()
                page_count += 1
                sleep(2)
            except KeyboardInterrupt:
                break

        return HREFS

    def collect_item_details(self, driver, HREFS):
        data_samples = []
        for href in HREFS:
            try:
                driver.get(href)
                title = driver.find_element(*self.data.title_tag).text
                print("[INFO]  title :", title)
                price = driver.find_element(*self.data.price_tag).text
                print("[INFO]  price :", price)
                asin = driver.find_element(*self.data.asin_tag).text
                print("[INFO]  asin :", asin)
                data_samples.append([href, title, price, asin])
            except NoSuchElementException as e:
                print(f"[ERROR] 要素が見つかりませんでした: {e}")
            except TimeoutException as e:
                print(f"[ERROR] タイムアウトが発生しました: {e}")

        return data_samples
