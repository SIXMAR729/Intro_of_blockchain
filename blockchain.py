from crypt import methods
import datetime
import json
import hashlib
from urllib import response
from flask import Flask, jsonify


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(nonce=1, previous_hash="0")
        self.create_block(nonce=10, previous_hash="10")
        self.create_block(nonce=30, previous_hash="20")


    def create_block(self, nonce, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "nonce": nonce,
            "previous_hash": previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, block):
        encode_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()
    
    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_proof = False
        while check_proof is False:
            hashoperation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashoperation[:4] == "0000":
                check_proof = True
            else:
                new_nonce+=1
        return new_nonce

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index<len(chain):
            block = chain[block_index] #Identify Block
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_nonce = previous_block["nonce"]
            nonce = block["nonce"] # Nonce of idetity Block
            hashoperation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
# Use Blockchain
blockchain = Blockchain()
print(blockchain.chain[0])
print(blockchain.chain[1])
print(blockchain.chain[2])
# hashing first block
print("Hashing first block is -> " + blockchain.hash(blockchain.chain[0]))
# hashing second block
print("Hashing second block is -> " +blockchain.hash(blockchain.chain[1]))
print("Hashing third block is -> " +blockchain.hash(blockchain.chain[2]))



#Web Server
app = Flask(__name__)

#Routing
@app.route('/')
def hello():
    return "<p>Hello Blockchain</p>"

@app.route('/get_chain', methods=["GET"])
def get_chain():
    response={
        "chain": blockchain.chain,
        "length":len(blockchain.chain)
    }
    return jsonify(response),200

@app.route('/mining', methods=["GET"])
def mening_block():
    #POW (Prove of Work)
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]
    #Nonce
    nonce = blockchain.proof_of_work(previous_nonce)
    #Previous Hash Block
    previous_hash = blockchain.hash(previous_block)
    #Update New Block
    blockchain.create_block(nonce, previous_hash)
    response={
        "message":"Mining Block Completed",
        "index":block["index"],
        "timestamp":block["timestamp"]
        "nonce":block["nonce"],
        "previous_hash"block["previous_hash"]
    }
    return jsonify(response), 200
#Run Server
if __name__ == "__main__":
    app.run()
