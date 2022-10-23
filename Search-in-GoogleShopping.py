from serpapi import GoogleSearch
from urllib.request import urlopen
# Imports
import pandas as pd
import json

# Initializing variables that gonna count
ID_qnt = 0
aux = 0
# Opening txt file to check number of lines ( 1 number per line)
arq = open('ids.txt', 'r')
for linha in arq:
    ID_qnt += 1

print("Numero de IDs no arquivo: ", ID_qnt)
arq.close()

manipulador = open('ids.txt',
                   'r')  # Put the name of txt file into 'archive.txt' content the numbers that you want to find
elements = manipulador.readlines()

elements = list(map(lambda s: s.strip(), elements))  # Removing all characters '/n' from txt file
print(elements)

while (aux < ID_qnt):
    search = elements[aux]
    params = {
        "q": search,
        "api_key": "Your API_KEY",  # Enter your API_KEY into " "
        "device": "desktop",
        "engine": "google",
        "google_domain": "google.com.br",
        "gl": "br",
        "hl": "pt",
        "location": "Brazil",
        "tbm": "shop"
    }

    search = GoogleSearch(params)  # Doing search with parameters passed in params{}
    results = search.get_dict()  # Getting the result like a dictionary
    link = results['search_metadata']['json_endpoint']  # Getting the result from 'search_metadata->json_endpoint' tab
    json_url = urlopen(link)
    data = json.loads(json_url.read())  # Passing the url with json file to data variable

    df = pd.DataFrame(data["shopping_results"])  # Start a dataframe with results in 'shopping_results' tab from json
    df = df.drop(["product_link", "product_id", "serpapi_product_api", "position", "thumbnail", "tag"],
                 axis=1)  # Take off some columns

    df.to_csv(f'{elements[aux]}.csv')  # Create csv file with the name contented in each line from txt file
    print("gerado arquivo com search =", {elements[aux]})  # Informs if csv file was create in the right way
    aux += 1
