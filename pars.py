from bs4 import BeautifulSoup
import requests
import csv

title_hir = []

headers = {
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.45'
}
def TurPars(url):
    response = requests.get(url=url, headers=headers)
    # print(response.status_code)
    # with open(file='index.html', mode='w', encoding="utf-8") as file:
    #     file.write(response.text)
    # with open(file='index.html') as file:
    #     src = file.read()

    soup = BeautifulSoup(response.content, "lxml")
    page = soup.find("nav", {'class': 'zng-pagination'}).get("data-total")
    pages = int(page)
    pages += 1

    for pan in range(1, pages):
        p = f'?page={pan}'
        res = requests.get(url=f'https://www.zingat.com/en/for-sale{p}', headers=headers)
        soup2 = BeautifulSoup(res.content, "lxml")
        get_li = soup.find_all('li', {'class': 'zl-card platin-border'})
        for li in get_li:
            get_link = li.find('a', {'class': 'zl-card-inner'})
            link = "https://www.zingat.com" + get_link.get("href")
            title = get_link.get("title")
            subtitle = get_link.get_text()
            # s = subtitle.replace("\n", " ")
            price = li.find('div', {'class': 'zlc-features'}).get_text()
            city = li.find('div', {'class': 'zlc-location'}).get_text()
            rooms = li.find('div', {'class': 'zlc-tags'})
            if rooms is None: continue
            room = rooms.get_text()
            r = room.replace("\n", " ")
            p = price.replace("\n", " ")
            c = city.replace("\n", "")
            title_hir.append(
                {
                    'Site': "zingat.com",
                    'Name': title,
                    'Price': p,
                    'City': c,
                    'Room': r,
                    'Url': link,
                }
            )
    with open('zinghat.txt', 'w', encoding="utf-8") as file:
        print(*title_hir, file=file, sep="\n")
    with open("zinghat.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=';')
        file_writer.writerow(['Site', 'Name', 'Price', 'City', 'Room', 'Url'])
        for hir in title_hir:
            file_writer.writerow(list(hir.values()))
    return print(len(title_hir))





def main():
    TurPars(url='https://www.zingat.com/en/for-sale')

if __name__ == "__main__":
    main()