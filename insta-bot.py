# 各モジュールを構成（なければcmdでpip install *** でインストール）
import asyncio
from cmath import exp
from concurrent.futures import process
from random import Random
import sys
from pyppeteer import launch
from pyppeteer.page import Page

userName = 'ischca'  # 'takatorea'
password = 'iamkuiiru'  # 'd79HsZ/LXH,ype,'
tagName = '春から大学生'

rand = Random()


async def waitRandom():
    delay = rand.randint(3, 12)
    await asyncio.sleep(delay)


async def select(page: Page, selector: str):
    await page.waitForSelector(selector)
    return await page.J(selector)


async def selectx(page: Page, selector: str):
    await page.waitForXPath(selector)
    return await page.Jx(selector)

"""
ログイン処理
"""


async def login(page: Page):
    print('ログイン中')
    # ログインID
    idInputName = 'username'
    # ログインID入力
    await (await select(page, f'[name={idInputName}]')).type(userName)

    # パスワード
    passInputName = 'password'
    # パスワード入力
    await (await select(page, f'[name={passInputName}]')).type(password)

    submit = await select(page, 'button[type=submit]')
    # ログインボタンクリック
    await submit.click()

    # 後での画面を待つ
    try:
        await page.waitForSelector('.coreSpriteKeyhole')
    except:
        # ログイン失敗の場合
        alert = await page.J('#slfErrorAlert')
        message = await page.evaluate('(e) => e.innerText', alert)
        print(message, file=sys.stderr)
        return False

    return True


async def goToPage(page: Page, url: str):
    # 指定ページへ遷移する
    return await asyncio.gather(
        page.goto(url),
        page.waitForNavigation()
    )


"""
指定回数分いいねしつづける
"""


async def repeatedlyLikes(page: Page, count: int = 200):
    print('いいね開始')
    # いいねしつづける
    likecount = 0  # カウントリセットで0代入
    while (likecount < count):  # count回ループする
        # いいねボタン取得
        heart = (await selectx(page,
                               '//div[@role="dialog"]//article//section//button/div/span/*[name()="svg" and contains(@aria-label, "いいね")]'))[0]
        ariaLabel = str(await page.evaluate('(e) => e.ariaLabel', heart))
        # いいね済み判定
        isDone = '取り消す' in ariaLabel
        if not isDone:
            # いいね済みでなければクリック
            await heart.click()
            likecount += 1
            # いいねした数を表示
            print("いいね")
            print(likecount)
        await waitRandom()
        # 次ボタンをクリック
        next = await selectx(page, '//div[@role="presentation"]//button//*[name()="svg" and contains(@aria-label, "次へ")]')
        await next[0].click()
    print('いいね終了')


async def main():
    # instagramにアクセス
    browser = await launch(args=['--no-sandbox', '--lang=ja-JP'])
    page = await browser.newPage()
    await goToPage(page, 'https://www.instagram.com/accounts/login/')

    # ログイン
    if await login(page):
        print('ログイン完了')
    else:
        print('ログイン失敗', file=sys.stderr)
        return

    # タグページへ遷移
    await goToPage(page, f'https://www.instagram.com/explore/tags/{tagName}/')
    print(f'#{tagName}を検索')

    # 最新の一つ目の投稿をクリック
    await (await selectx(page, '//article/h2/following-sibling::div[1]/div[1]/div[1]/div[1]/a[1]'))[0].click()
    print('投稿を表示')

    # いいねする
    await repeatedlyLikes(page, 200)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
