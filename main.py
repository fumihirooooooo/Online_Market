#Commom.Module
from Common.ToGspread import ToGspread
from Common.Configs import Configs
from Common.GetInfo import GetInfo

from selenium import webdriver #webブラウザの制御
from selenium.webdriver.chrome.options import Options #Chromeブラウザの動作をカスタマイズ
from selenium.common.exceptions import NoSuchElementException  #指定した要素が見つからない場合に発生する



def main(tag,get_info_func):
    results = get_info_func(tag)
    
    for result in results:
        print(result)
    
   # Gspreadに出力するTogspreadファイル参照
    to_gspread = ToGspread (results, "フットサルシューズ情報.xlsx")
    to_gspread.list_to_gspread()    
    
def get_amazon_info(tag):
    getinfo = GetInfo(data = tag)
    return getinfo.get_info_data()

if __name__ == "__main__":
    tag = Configs() #Configsを呼び出す
    main(tag, get_amazon_info)