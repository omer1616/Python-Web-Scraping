import requests
from bs4 import BeautifulSoup
import json


# url = "https://www.trendyol.com/laptop-x-c103108"
# response = requests.get(url)
# print(response.status_code)


class ScrapingTrendyol:
    def __init__(self):
        self.url = "https://www.trendyol.com"

    def get_html_source(self, param=None):
        payload = {'pi': param}
        response = requests.get(self.url + "/laptop-x-c103108", params=payload)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        return response.status_code

    def get_products(self, source: object = None) -> object:
        soup = self.get_html_source(source)
        products = soup.find('div', attrs={'class': 'prdct-cntnr-wrppr'}).find_all("div", attrs={
            'class': "p-card-wrppr with-campaign-view"})
        return products

    def get_product_name(self, source=None):
        products = self.get_products(source)
        product_names = list(
            map(lambda product_name: product_name.find("div", attrs={"class": "product-down"}).find("span").text,
                products))

        return product_names

    def get_product_link(self, source=None):
        products = self.get_products(source)
        product_links = list(
            map(lambda product_link: self.url + "{}".format(product_link.find("a").get("href")), products))

        return product_links

    def get_product_info(self, source=None):
        products = self.get_products(source)
        product_infos = list(
            map(lambda product_name: product_name.find("div", attrs={"class": "product-down"}).find_all("span")[1].text,
                products))
        product_prices = list(
            map(lambda product_name: product_name.find("div", attrs={"class": "prc-box-dscntd"}).text,
                products))
        print(len(product_prices))
        product_info_list = [
            {"ProductDesc": product_info, "ProductPrice": product_price} for product_info, product_price in
            zip(product_infos, product_prices)]

        return product_info_list

    def merge_product(self):
        product_names = self.get_product_name()
        product_links = self.get_product_link()
        product_infos = self.get_product_info()

        product_list = [
            {"ProductName": product_name, "ProductLink": product_link, "ProductInfos": [product_info]} for
            product_name, product_link, product_info in zip(
                product_names, product_links, product_infos)]

        return product_list

    def save_json(self, data):
        with open('products.json', "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=3, ensure_ascii=False))
            print("başarılı")

    # def save_products_link(self, source=None):
    #
    #     products_info_dict = [
    #         {'ProductName': product_name, 'ProductLink': product_link} for product_name, product_link in zip(
    #             product_names, product_links)]
    #     print(products_info_dict)
    #     print("**" * 50)
    #     for i in products_info_dict:
    #         print(i)
    #     products_info_dict = json.dumps(products_info_dict, indent=3)
    #
    #     print("**" * 50)
    #     print(products_info_dict)


if __name__ == "__main__":
    scraping = ScrapingTrendyol()
    print(scraping.get_html_source())
    print(scraping.get_products())
    print(scraping.get_product_link())
    print(scraping.get_product_name())
    # data = scraping.merge_product()
    print(scraping.get_product_info())
    # print(scraping.save_json(data))
    # print(scraping.get_html_source())
