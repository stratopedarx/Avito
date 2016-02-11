# -*- coding: utf-8 -*-

import requests
from lxml import html
import urlparse
import smtplib


class Avito:
    MAX_SUM = 2500000
    MIN_SUM = 1400000

    RESULT = []

    def parse_avito_RUN(self):
        url = "https://www.avito.ru/dzerzhinsk/kvartiry/prodam/2-komnatnye/vtorichka?bt=0&f=59_13988b"
        r = requests.get(url)
        res = html.fromstring(r.content)
        result = res.xpath(u'//*[contains(text(), "Последняя")]/@href')
        print '1', result
        num = self._get_page_num(result[0])
        print '3', num
        result = self.get_page_data(num)
        print '8', result

    def _get_page_num(self, href):
        result = urlparse.urlparse(href)
        print '2', result.query
        result = urlparse.parse_qs(result.query)
        return int(result['p'][0])

    def get_page_data(self, num):
        url = "https://www.avito.ru/dzerzhinsk/kvartiry/prodam/2-komnatnye/vtorichka?p={}bt=0&f=59_13988b"
        for i in xrange(1, num):
            r = requests.get(url.format(i))
            print '4', r
            self.get_all(r.content)
        return self.RESULT

    def get_all(self, data):
        data = self._get_desc(data)
        print '6', data
        for key, i in enumerate(data):
            href = i.xpath('//h3[@class="title"]/a/@href')[key]
            # title = i.xpath('//h3[@class="title"]/a/@title')[key]
            # adress = i.xpath('//p[@class="address fader"]/text()')[key]
            price = i.xpath('//div[@class="about"]/text()')[key]
            price = price.strip()
            if price:
                price = price.split(' ')
                price.pop()
                price = ''.join(price)
                summ = int(price)
                print '7', price
                if summ > self.MAX_SUM and summ < self.MIN_SUM:
                    continue
            else:
                price = u'Без цены'
            self.RESULT.append({"href": 'https://www.avito.ru' + href,

                                "price": price,  # "adress": adress, "title": title,
                                })

    def _get_desc(self, data):
        return self.get_from_xpath(data, './/div[@class="description"]')

    def get_from_xpath(self, data, xpath):
        res = html.fromstring(data)
        print '5', res
        return res.xpath(xpath)


if __name__ == '__main__':

    avito = Avito()
    avito.parse_avito_RUN()
    msg = u'2 комнатные квартиры в Дусте' + '\n'
    for res in avito.RESULT:
        for key, value in res.items():
            print key, '=====', type(res[key])
            msg += str(res[key]) + '\n'
            print msg
        msg += '-' * 50
    server = smtplib.SMTP('smtp.mail.ru', 587)
    server.starttls()
    server.login("stratopedarx@mail.ru", "stratopedarx1")
    server.sendmail("stratopedarx@mail.ru", "stratopedarx@mail.ru", msg)
    server.quit()

    # unicode.encode(unicode(str(s), 'cp1251'), 'utf8')
