import sqlite3
from web3 import Web3

class Voter:
    def __init__(self, ssn, driver_id, zipcode, voter_account, private_key, contract):
        self.ssn = ssn
        self.driver_id = driver_id
        self.zipcode = zipcode
        self.voter_account = voter_account
        self.private_key = private_key
        self.contract = contract

    def login(self):
        conn = sqlite3.connect('database/voting_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM voters WHERE ssn=? AND driver_id=? AND zipcode=?", 
                       (self.ssn, self.driver_id, self.zipcode))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def view_elections(self):
        conn = sqlite3.connect('database/voting_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM elections WHERE is_active=1")
        elections = cursor.fetchall()
        conn.close()
        return elections

    def cast_vote(self, candidate_id):
        transaction = self.contract.functions.castVote(candidate_id).buildTransaction({
            'from': self.voter_account,
            'nonce': Web3.eth.get_transaction_count(self.voter_account),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
        })
        signed_txn = Web3.eth.account.sign_transaction(transaction, self.private_key)
        tx_hash = Web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Vote transaction hash: {tx_hash.hex()}")
