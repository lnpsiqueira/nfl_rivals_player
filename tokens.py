import requests
import pandas as pd

print("Downloading the original search results")
url = 'https://explorer.mythical.market/api/transactions?filter=(%20transactionType%20eq%20ContractCreation%20)'
response = requests.get(url)
data = response.json()
total_pages = data['paging']['totalPages']

# If data['next'] isn't empty, let's download the next page, too
total_results = []
page = 0
while page <= total_pages:
    print("Next page found, downloading", page)
    response = requests.get(url + '&page=' + str(page))
    data = response.json()
    page += 1
    for player in data['data']:
        try:
            print(player["toLinks"][2]['display'])
        except:
            continue
    total_results = total_results.append(data)


url_tokens = 'https://explorer.mythical.market/api/tokens?size=10000'
response = requests.get(url_tokens)
tokens_data = response.json()
total_pages = data['paging']['totalPages']

for player in tokens_data['data']:
    try:
        print(player["addressLinks"][2]['display'], player["totalSupply"])
    except:
        continue

dataframe = pd.json_normalize(tokens_data, record_path=['data'])
dataframe = dataframe.explode('addressLinks')
dataframe = pd.concat([dataframe.drop(['addressLinks'], axis=1), dataframe['addressLinks'].apply(pd.Series)], axis=1)
dataframe = dataframe.loc[dataframe['rel'] == 'token']
