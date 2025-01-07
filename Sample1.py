#Commom.Module
from ToExcel import ToExcel

# import
from selenium import webdriver #webブラウザの制御
from selenium.webdriver.chrome.options import Options #Chromeブラウザの動作をカスタマイズ
import chromedriver_binary #Chromeを使用するためのバイナリ（CPが直接実行可能な）ファイル
from selenium.common.exceptions import NoSuchElementException  #指定した要素が見つからない場合に発生する

# wait
from selenium.webdriver.support import expected_conditions as EC #Web ページ上で特定のイベントが発生するまで待機
from selenium.webdriver.support.ui import WebDriverWait     #特定の条件が満たされるまで Web ページ上で待機

# selenium 4.0 ↑
from selenium.webdriver.common.by import By  #Web ページ上の要素を特定するための定数を提供(例: ID、CSS セレクターなど)
from time import sleep

#chrome optionsの設定
chrome_options = Options()#
# chrome_options.add_argument('--headless')  #headlessモードの有効化
#chrome driverの起動
driver = webdriver.Chrome(options=chrome_options) 

HREFS = []
results = []

# URL開く:Amazonのトップページを開く
driver.get("https://www.amazon.co.jp/ref=nav_logo")
# 待機処理

# driver.implicitly_wait(10)　#暗黙的待機（指定された時間内に要素が表示されるまで待機、WebDriver の implicit_wait 属性を設定）最大10秒まで待機する設定
sleep(2)
wait = WebDriverWait(driver=driver, timeout=60)  #明示的な待機。特定の条件が満たされるまで待機。WebDriverWait クラスを使用

#検索窓
Word = "フットサルシューズ"
driver.find_element(By.ID, "twotabsearchtextbox").send_keys(Word)
sleep(1)
driver.find_element(By.ID,"nav-search-submit-button").click()

#商品URLの取得
URLS = driver.find_elements(By.CSS_SELECTOR,"a.a-link-normal.s-no-outline")

#取得したURL情報をHREFSリストへ追加
for URL in URLS:
    URL = URL.get_attribute("href")
    print("[INFO] URL :", URL)
    HREFS.append(URL)
    
#商品詳細の取得
#HREFSリストの書くURLに対して商品ページにアクセス
for HREF in HREFS:
    try:
        driver.get(HREF)
        # title：ID: productTitle
        title = driver.find_element(By.ID, "productTitle").text
        print("[INFO]  title :", title)
        # price：CSSセレクタ: div.aok-align-center > span > span > span.a-price-whole
        price = driver.find_element(By.CSS_SELECTOR,"span.a-price-whole").text
        print("[INFO]  price :", price)
        #
        
        # # img
        # img = driver.find_element(By.XPATH, '//div[@id="imgTagWrapperId"]/img').get_attribute("src")
        # print("[INFO]  img :", img)
        results.append([HREF,title, price])
        
    except NoSuchElementException as e:
        print(f"[ERROR]要素が見つかりませんでした: {e}")

# Excelに出力するToExcelファイル参照
to_excel = ToExcel(results, "フットサルシューズ情報.xlsx")
to_excel.list_to_excel()   