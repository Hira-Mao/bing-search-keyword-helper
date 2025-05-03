from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os

# Googleのトップページ
URL = 'https://www.google.co.jp'

def main():
    '''
    Googleでキーワードを検索し、検索結果の1ページ目に指定ドメインが含まれていないキーワードを抽出
    '''

    # ファイルからキーワードとドメインを読み込む
    with open(os.path.join(os.path.dirname(__file__), '検索キーワードリスト.txt'), encoding='utf-8') as f:
        keywords = [s.strip() for s in f if s.strip()]

    with open(os.path.join(os.path.dirname(__file__), 'ドメインリスト.txt'), encoding='utf-8') as f:
        domains = [s.strip() for s in f if s.strip()]

    # ブラウザ設定
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = ChromeService(executable_path="/Users/m/Desktop/chromedriver")  # 自分のパスに合わせて修正
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))

    ok_keywordlist = []

    for keyword in keywords:
        search(keyword, driver)
        urls = get_url(driver)
        domain_checked(urls, domains, ok_keywordlist, keyword)

    # 結果を保存
    with open('結果.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(ok_keywordlist))

    driver.quit()


def search(keyword, driver):
    '''
    Google検索ボックスにキーワードを入力して検索
    '''
    input_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )
    input_element.clear()
    input_element.send_keys(keyword)
    input_element.send_keys(Keys.RETURN)
    time.sleep(2)


def get_url(driver):
    '''
    検索結果のリンクを全取得し、URLだけをリストにして返す
    '''
    urls = []
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a'))
    )

    for el in elements:
        href = el.get_attribute('href')
        if href and href.startswith('http') and 'google' not in href:
            urls.append(href)

    return urls


def domain_checked(urls, domains, ok_keywordlist, keyword):
    '''
    取得したURLのドメインが指定リストに含まれていないかチェック
    '''
    for url in urls:
        m = re.search(r'//(.*?)/', url)
        if not m:
            continue
        domain = m.group(1)
        if domain.startswith('www.'):
            domain = domain[4:]
        if domain in domains:
            print(f'キーワード「{keyword}」の検索結果には大手ドメインがありましたので除外します。')
            return  # 一致したら即終了

    # どのドメインにも一致しなかったら追加
    ok_keywordlist.append(keyword)

if __name__ == "__main__":
    main()
