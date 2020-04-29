import bs4
import glob
import os
import re
import requests
import time
import tldextract

from collections import defaultdict
from requests.exceptions import MissingSchema
from lxml import html
from urllib.parse import urlparse

def clear_files(path='output/*'):
    """
    Removes existing files from the output file directory
    :param path:
    :return:
    """
    files = glob.glob(path)
    for file in files:
        os.remove(file)

class Crawler(requests.Session):

    LINK_COUNT = 25

    def __init__(self):
        super().__init__()
        self.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        })
        self.seen_names = defaultdict(int)

    def get(self, url, **kwargs):
        """
        Custom get request that uses the request module's get with the difference being we try a request up to 3 times
        on failure before raising an exception.
        """
        count = kwargs.get('count') or 0
        response = super().get(url, **kwargs)
        count += 1
        if response.status_code not in [200, 302] and count < 3:
            time.sleep(3)
            kwargs['count'] = count
            return self.get(url, **kwargs)
        elif response.status_code not in [200, 302]:
            raise Exception(f"Response status code: {response.status_code}. Request failed, try again later.")
        return response


    def get_links(self, page, domain_root, unique, count):
        """
        Retrieves the specified number of links from the page - unique links if specified
        :param page: lxml html object
        :param domain_root: domain name that is being searched
        :param unique: boolean determining if user only wants unique links
        :param count: number of links to be returned
        :return: list of link elements - <a> tags
        """
        if unique:
            return list(set(page.xpath(f'.//a[contains(@href, "{domain_root}")]')))[:count]
        return page.xpath(f'.//a[contains(@href, "{domain_root}")]')[:count]

    def normalize_file_name(self, file_name):
        """
        Normalize the file name to be more human readable and file path appropriate
        :param file_name: raw name of the file
        :return: normalized name
        """
        normalized_name = re.sub('[^0-9a-zA-Z]', '_', file_name).strip('_')
        if normalized_name in self.seen_names:
            # Repeat name, add a count to it
            normalized_name = f"{normalized_name}_{self.seen_names[normalized_name] + 1}"
        self.seen_names[normalized_name] += 1
        return f"{normalized_name}.html"

    def generate_file_name(self, link):
        """
        Generate the name of the file from the link
        :param link: link tag
        :return: file name
        """
        parsed_url = urlparse(link.get('href'))
        file_name = link.text or parsed_url.path
        if file_name == '/':
            file_name = link.get('href')
        return self.normalize_file_name(file_name)

    def output_to_html(self, links):
        """
        Iterate through the links and to each page then render the html content to html files
        :param links:
        :return:
        """
        for link in links:
            file_name = self.generate_file_name(link)
            response = self.get(link.get('href'))
            page_html = bs4.BeautifulSoup(response.content, 'html.parser')
            with open(os.path.join('output', file_name), 'w') as html_file:
                html_file.write(str(page_html))

    def crawl(self, url, headers={}, **kwargs):
        """
        Handle the web crawling process from fetching the base page to calling the function to output the results
        :param url: URL of the website
        :param headers: Any custom headers
        :param kwargs: unique and count key words for further user customization
        :return:
        """
        if headers:
            self.headers.update(headers)
        try:
            response = self.get(url)
        except MissingSchema:
            print(f'Please enter a URL with a valid schema such as https://{url} or http://{url}')
            return

        count = kwargs.get('count') or Crawler.LINK_COUNT
        unique = kwargs.get('unique') or False
        clear = kwargs.get('clear')

        if clear:
            clear_files()

        page = html.fromstring(response.content)
        parsed_url = tldextract.extract(url)
        domain = parsed_url.domain
        links = self.get_links(page, domain, unique=unique, count=count)
        self.output_to_html(links)


if __name__ == "__main__":
    url = "https://www.yahoo.com"
    crawler = Crawler()
    crawler.crawl(url, clear=True)