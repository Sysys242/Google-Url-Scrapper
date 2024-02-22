import tls_client
from urllib.parse import urlparse



class Google:
    def __init__(self) -> None:
        self.session = tls_client.Session(client_identifier='chrome_112')
        self.keywords_list = open('./keywords.txt', 'r', encoding="utf-8").read().splitlines()
        self.scrapped = []
    
    def scrape(self, keyword:str, page:int) -> str:
        page = page*10
        return self.session.get(
            f'https://www.google.com/search?q={keyword}&start={page}',
            headers={
                'authority': 'www.google.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'accept-language': 'fr-FR,fr;q=0.5',
                'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"15.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'sec-gpc': '1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            }
        ).text
    
    def extractUrlFromStr(self, text:str) -> dict:
        urls = []
        textSplitted = text.split('ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=')
        for split in textSplitted:
            url = split.split('"')[0]
            if not "google.com" in url and not "html" in url.lower():
                urls.append(url)
        return urls
    
    def getDomainFromUrl(self, url:str) -> str:
        url = urlparse(url)
        domain = url.netloc
        return domain
    
    def checkDupe(self, url:str) -> bool:
        domain = self.getDomainFromUrl(url)
        if domain in self.scrapped:
            return True
        else:
            self.scrapped.append(domain)
            return False
    
    def runScrapper(self):
        for keyword in self.keywords_list:
            for page in range(0,98):
                scrapped = self.scrape(keyword, page) # replace for remove it to append idk bc shit split
                open('res.txt', 'w', encoding="utf-8").write(scrapped)
                if 'Aucun document ne correspond aux termes de recherche spécifiés' in scrapped:
                    print(f'Finished Scrapping: {keyword} - {(page/10)-1}')
                    break
                for url in self.extractUrlFromStr(scrapped):
                    if not self.checkDupe(url):
                        url = f"https://{self.getDomainFromUrl(url)}/"
                        open('urls.txt', 'a', encoding="utf-8").write(f'{url}\n')
                        print(f'New Url: {url}')
                    else:
                        print(f"Dupe Detected: {url}")

if __name__ == "__main__":
    googleClient = Google()
    googleClient.runScrapper()
