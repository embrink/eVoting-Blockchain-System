# File: config.py
# Purpose: This file provides functions to set up a connection with the blockchain using Web3, load the smart contract ABI, and initialize the contract with the contract address.
# Authors: Ella Brink, Lauren Wilson, Emma Bellai, Lucy DiSalvo
# Version History:
# - Version 1.0 (Sprint 3): Initial version created by Ella Brink
# - Version 1.1 (Sprint 4): Added documentation by Lucy DiSalvo 

from web3 import Web3
import json

# Blockchain setup
def get_web3():
    return Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

def load_contract():
    with open("blockchain/contract_abi.json") as abi_file:
        abi = json.load(abi_file)
    with open("blockchain/contract_address.txt") as address_file:
        address = address_file.read().strip()
    web3 = get_web3()
    return web3.eth.contract(address=address, abi=abi)
