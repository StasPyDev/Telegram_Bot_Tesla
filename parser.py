import requests
from bs4 import BeautifulSoup as BS


# Returns a page for the parser
def return_soup(url, headers):
    html = requests.get(url=url, headers=headers).text

    soup = BS(html, 'lxml')
    return soup


# Number of pages to go through
def paginations(soup):
    pagination = soup.find('div', class_='paginate').find_all('span', class_='page')[-1].get_text()
    return pagination


# Parse first post for publication
def parse_first_post(headers):
    data = []
    soup = return_soup(url='https://www.tesmanian.com/blogs/tesmanian-blog', headers=headers)
    first_post = soup.find('div', class_='five columns alpha')
    title = first_post.find('a').get('title')
    link_post = 'https://www.tesmanian.com' + first_post.find('a').get('href')

    data.append({
        'Title': title,
        'URL': link_post
    })
    return data


# Collects information from other posts
def get_post_information(paginate, headers, posts, page_post):
    for page in range(page_post, int(paginate)):
        data = []
        url = f'https://www.tesmanian.com/blogs/tesmanian-blog?page={page + 1}'

        soup = return_soup(url=url, headers=headers)

        if parse_first_post(headers=headers)[0]['Title'] not in posts:
            return parse_first_post(headers=headers), page_post
        else:
            block_contents = soup.find_all('div', class_='five columns alpha')
            for content in block_contents:
                title = content.find('a').get('title')
                link_post = 'https://www.tesmanian.com' + content.find('a').get('href')
                if title not in posts:
                    data.append({
                        'Title': title,
                        'URL': link_post
                    })
                    return data, page_post
                else:
                    continue
            page_post += 1


def parse(posts, page_post):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

    soup = return_soup(url='https://www.tesmanian.com/blogs/tesmanian-blog', headers=headers)
    paginate = paginations(soup=soup)

    data, page_post = get_post_information(paginate=paginate, headers=headers, posts=posts, page_post=page_post)
    return data, page_post
