from coinbase.wallet.client import Client

def get_keys():
    with open('keys.txt', 'r') as file:
        return file.read().splitlines()


key, secret = get_keys()
client = Client(key, secret)