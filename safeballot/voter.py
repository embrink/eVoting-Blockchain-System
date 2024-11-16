# File: voter.py
# Purpose: This file defines the Voter class, which handles voter authentication, viewing active elections, and casting votes on the blockchain.
# Authors: Ella Brink, Lauren Wilson, Emma Bellai, Lucy DiSalvo
# Version History:
# - Version 1.0 (Sprint 2): Initial version created by Ella Brink
# - Version 1.1 (Sprint 4): Added Web3 functionality for voting and database interaction by Lucy DiSalvo
# - Version 1.2 (Sprint 4): Added documentation by Lucy DiSalvo 
# - Version 1.3 (Sprint 4): Updated voter information, added contract_address, contract_abi, 
# and provider_url for blockchain/ganache integration by Lucy DiSalvo


import sqlite3
from web3 import Web3

class Voter:
    def __init__(self, ssn, driver_id, zipcode, voter_account, private_key, contract_address, contract_abi, provider_url='http://localhost:7545'):
        self.ssn = ssn
        self.driver_id = driver_id
        self.zipcode = zipcode
        self.voter_account = voter_account
        self.private_key = private_key
       
        # Connect to the Ethereum network (replace with your network provider URL)
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        
        # Make sure web3 is connected
        if not self.web3.isConnected():
            raise Exception("Failed to connect to Ethereum network")
        
        # Set up the contract
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)

    def login(self):
        """
        Authenticate the voter using the provided SSN, driver ID, and zipcode.
        """
        conn = sqlite3.connect('database/voting_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM voters WHERE ssn=? AND driver_id=? AND zipcode=?", 
                       (self.ssn, self.driver_id, self.zipcode))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def cast_vote(self, candidate_id):
        """
        Cast a vote for a candidate by sending a transaction to the smart contract.
        """
        # Ensure the contract has a function named `castVote` that accepts a candidate ID
        # Build the transaction for voting
        transaction = self.contract.functions.castVote(candidate_id).buildTransaction({
            'from': self.voter_account,
            'nonce': self.web3.eth.getTransactionCount(self.voter_account),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })
        
        # Sign the transaction using the private key
        signed_txn = self.web3.eth.account.signTransaction(transaction, self.private_key)
        
        # Send the signed transaction
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        
        # Return the transaction hash (for logging or confirmation)
        print(f"Vote transaction hash: {tx_hash.hex()}")
        return tx_hash.hex()
