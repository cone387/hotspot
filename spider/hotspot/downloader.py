from cone.spider_ex import CrawlerRequest, HttpDownloader


HEADERS = CrawlerRequest.headers.copy()
HEADERS['Content-Type'] = 'application/x-www-form-urlencoded'

DATA = {
    'method': 'GET',
    'headers': CrawlerRequest.headers.copy(),
}


class Response():

    def __init__(self, response):
        try:
            json_text = response.json()
        except:
            json_text = {'status_code': 600}
        if json_text['status_code'] >= 200 and json_text['status_code'] < 400:
            self.status_code = 200
        else:
            self.status_code = json_text['status_code']
        self.text = json_text.get('content', '')
        self.url = json_text.get('url')
        self.content = response.content


class NewsDownloader(HttpDownloader):

    pass