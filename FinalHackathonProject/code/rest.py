import requests

recent = "https://mempool.space/api/mempool/recent"
response = requests.get(recent).json()

txid = response[1]['txid']
fee = response[0]['fee']

print(txid)

recent_tx = "https://mempool.space/api/tx/" + txid
response = requests.get(recent_tx).json()
#print(response)
size = response['size']
# print(size)

weight = response['weight']
# print(weight)

# weight = response['block_height']
# print(response)


# recent_transactions = json.loads(recent_api.json())

# print(recent_transactions.json()[0])

# api_url_tx = "https://mempool.space/api/tx/"
difficulty = "https://mempool.space/api/v1/difficulty-adjustment"
response = requests.get(difficulty).json()
# print(response)

block_tip_height = "https://mempool.space/api/blocks/tip/height"
response = requests.get(block_tip_height).json()
# print(response)

# block = "https://mempool.space/api/block/" + hash
# response = requests.get(difficulty)
# print(response.json())
