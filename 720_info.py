import requests, json
from bs4 import BeautifulSoup as BS

def get_html():
    index_count = 1
    for i in range(0, 721, 20):
        url = f"https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}"

        r = requests.get(url)
        with open(f'html_data/page_{index_count}.html', 'w', encoding='utf-8') as file:
            file.write(r.text)

        index_count += 1

def get_data():
    index_count = 1
    iteration = 1

    data = []
    for i in range(0, 721, 20):

        with open(f'html_data/page_{index_count}.html', encoding='utf-8') as file:
            html = file.read()

        soup = BS(html, 'lxml')
        hrefs = soup.find_all('div', class_='bt-slide-content')

        for href in hrefs:
            link = href.find('a').get('href')

            r = requests.get(link)
            soup = BS(r.content, 'lxml')

            person_company_names = soup.find(class_='col-xs-8 col-md-9 bt-biografie-name').find('h3').text.split(',')
            person_name, company_name = person_company_names[0].strip(), person_company_names[1].strip()
            person_links = []

            try:
                links = soup.find(class_='col-xs-12 col-md-4').find('ul').find_all('li')
                for link in links:
                    person_links.append(link.find('a').get('href'))
            except Exception:
                person_links = None

            data.append(
                {
                    'person_name': person_name,
                    'company_name': company_name,
                    'social_networks': person_links
                }
            )
            print(f"Iteration #{iteration} - was completed!")
            iteration += 1

        index_count += 1

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    # get_html()
    get_data()

if __name__ == '__main__':
    main()

