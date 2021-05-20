from requests import get


class Connect:
    def __init__(self, stream=True, timeout=5, proxies=None):
        self.stream = stream
        self.timeout = timeout
        self.proxies = proxies

    def get(self, url):
        num = 0
        while(num <= 6):
            try:
                response = get(url, stream=self.stream, timeout=self.timeout, proxies=self.proxies)
            except:
                num += 1
                print('Try to connect...(count {} )'.format(num))
            else:
                break
        else:
            exit('connect error!')
        return response
