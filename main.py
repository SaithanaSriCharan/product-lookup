import requests, json
from bs4 import BeautifulSoup
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ajio/search/{barcode}")
def read_item(barcode: int):
    #Search for the product on AJIO
    search_url = f'https://www.ajio.com/search/?text={barcode}'
    response = requests.get(search_url)

    # Check if the request was successful
    if response.status_code != 200:
        return {"status_code":response.status_code,"reason":response.reason}
    
    #Parse the search results
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #Extract product details (you need to adjust this based on AJIO's HTML structure)
    products = {}
    for item in soup.find_all('script', type='application/ld+json'):
        try:
            products = json.loads(item.text)
            if products['@type'] != 'ProductGroup':
                products = []
        except Exception as e:
            continue
    if products:
        products['url'] = "https://www.ajio.com/p/"+products['productGroupID']
    else:
        response.status_code = 404
        response.reason = "No Product Found"
    return {"status_code":response.status_code,"reason":response.reason, "result":products}
