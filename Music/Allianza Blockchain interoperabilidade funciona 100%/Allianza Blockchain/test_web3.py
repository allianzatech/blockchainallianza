from web3 import Web3

uri = "https://sepolia.infura.io/v3/20dc4d008abf4fcbbe5b0991323f8184"  # Substitua por sua chave real
w3 = Web3(Web3.HTTPProvider(uri))
print("Conectado:", w3.is_connected())