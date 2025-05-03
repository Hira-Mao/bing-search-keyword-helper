import requests
from bs4 import BeautifulSoup
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

def search_bing(keyword):
    headers = {"User-Agent": random.choice(user_agents)}
    query = keyword.replace(" ", "+")
    url = f"https://www.bing.com/search?q={query}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("検索に失敗しました")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for item in soup.select(".b_algo h2 a")[:3]:
        title = item.get_text()
        link = item.get("href")
        results.append((title, link))

    return results

def main():
    while True:
        keyword = input("🔍 検索キーワードを入力してください（終了: q）: ")
        if keyword.lower() == 'q':
            break

        results = search_bing(keyword)
        if not results:
            print("結果が見つかりませんでした。\n")
        else:
            print(f"\n【{keyword}】の検索結果（上位3件）:")
            for i, (title, link) in enumerate(results, start=1):
                print(f"{i}. {title}\n   {link}")
            print("")

if __name__ == "__main__":
    main()
