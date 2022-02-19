from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import sys

# 要素を待機し、取得するwaiterを生成する
class Waiter:

    # 要素を待機する秒数
    waitSecond: int
    # WebDriverWaitインスタンス
    waiter: WebDriverWait

    # コンストラクタ
    def __init__(self, driver: webdriver, waitSecond: int = 10):
        super().__init__()

        # 要素を待機する秒数を設定
        self.waitSecond = waitSecond

        # WebDriverWaitインスタンス取得
        self.waiter = WebDriverWait(driver, waitSecond)
    
    # 要素が読み込まれるまで待機し、要素を取得する
    def wait(self, locatorStrategy: str, key: str):
        try:
            return self.waiter.until(EC.presence_of_element_located((locatorStrategy, key)))
        except TimeoutException:
            print('要素の取得に失敗しました')
            sys.exit()
    