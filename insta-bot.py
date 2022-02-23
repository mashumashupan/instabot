# 各モジュールを構成（なければcmdでpip install *** でインストール）
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import urllib.parse
import time
import waiter as wt

userName = 'haru__pppp'  # 'takatorea'
password = 'demain2049'  # 'd79HsZ/LXH,ype,'
driver: webdriver
waiter: wt.Waiter


def loadText(fileName: str) -> [str]:
    # ファイルをオープンする
    rivalsText = open(fileName)

    # 行ごとにすべて読み込んでリストデータにする
    rivals = rivalsText.readlines()

    # ファイルをクローズする
    rivalsText.close()

    return rivals


"""
ログイン処理
"""


def login(id: str, pw: str):
    # ログインID
    idInputName = 'username'
    userNameInput = waiter.wait(By.NAME, idInputName)
    # ログインID入力
    userNameInput.send_keys(id)

    # パスワード
    passInputName = 'password'
    passwordInput = waiter.wait(By.NAME, passInputName)
    # パスワード入力
    passwordInput.send_keys(pw)
    passwordInput.send_keys(Keys.ENTER)

    # ポップアップの後でを選択
    elem_search_word = waiter.wait(
        By.XPATH, '//div[@role="dialog"]//button[contains(text(), "後で")]').click()
    driver.implicitly_wait(2)
    return


"""
指定回数分いいねしつづける
"""


def repeatedlyLikes(count: int = 200):
    # いいねしつづける
    likecount = 0  # カウントリセットで0代入
    while (likecount < count):  # count回ループする
        driver.implicitly_wait(4)
        # いいねボタン取得
        heart = waiter.wait(
            By.XPATH, '//div[@role="dialog"]/article/div[2]/section//button[*[name()="svg" and contains(@aria-label, "いいね")]]')
        # いいね済み判定
        isDone = '取り消す' in heart.find_element_by_xpath(
            '*[name()="svg"]').get_attribute('aria-label')
        if not isDone:
            # いいね済みでなければクリック
            heart.click()
            likecount += 1
            # いいねした数を表示
            print("いいね")
            print(likecount)
        # 次ボタンをクリック
        elem_search_word = driver.find_element_by_css_selector(
            "a.coreSpriteRightPaginationArrow").click()
    print("200いいね!")


def main():
    """
    ここからは自動アクションになります。
    """

    # ライバル一覧を読み込む
    rivalsList = loadText('rivals.txt')

    # instagramにアクセス
    global driver
    driver = webdriver.Chrome('/opt/chrome/chromedriver')
    driver.get("https://www.instagram.com/accounts/login/")

    # Waiterインスタンス生成
    global waiter
    waiter = wt.Waiter(driver)

    # ログイン
    login(userName, password)

    # 検索窓をアドレスバーに直接入力今回は「photo」にした
    driver.get(rivalsList[0])

    # フォロワーを表示
    waiter.wait(
        By.XPATH, '//main//header//section//a[contains(text(), "フォロワー")]').click()
    waiter.wait(
        By.XPATH, '//div[@role="dialog"]//ul//li//div[@role="button"]/a')
    while (True):
        top = driver.execute_script(
            "return document.querySelector('.isgrP').scrollTop")
        print(top)
        height = driver.execute_script(
            "return document.querySelector('.isgrP').scrollHeight")
        print(height)
        if(top == height):
            break
        else:
            driver.execute_script(
                "document.querySelector('.isgrP').scrollTop = document.querySelector('.isgrP').scrollHeight")
    # フォロワーをリストで取得
    # rivalFollowers = waiter.wait(By.XPATH, '//div[@role="dialog"]//ul//li//div[@role="button"]/a/@href')

    # print(rivalFollowers)

    # 一つ目の投稿をクリック
    #waiter.wait(By.XPATH, "//article/div[1]/div[1]/div[1]/div[1]/div[1]/a").click()

    # いいねする
    # repeatedlyLikes(3)


if __name__ == '__main__':
    main()
