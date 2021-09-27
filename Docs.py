

class Docs:
    def __init__(self, num, url, text):
        self.num = num
        self.url = url
        self.text = text


    def get_text(self):
        return self.text

    def get_url(self):
        return self.url

    def get_num(self):
        return self.num
