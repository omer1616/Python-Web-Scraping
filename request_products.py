import requests


class Product:
    def __init__(self) -> None:
        self.url = 'https://dummyjson.com/products'

    def get_all_product(self):
        response = requests.get(self.url)
        return response.json()

    def get_single_product(self, product_id):
        response = requests.get(f"{self.url}/{product_id}")
        return response.json()

    def search_product(self, name):
        payload = {'q': name}
        response = requests.get(f"{self.url}/search", params=payload)
        return response.json()


product = Product()
# print(product.get_all_product())  
print(product.search_product('phone'))
