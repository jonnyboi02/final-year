from hashlib import sha256
import json
import time

#https://gitlab.com/dsblendo/blockchain/-/blob/master/Blockchain.py
#https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/
#https://www.section.io/engineering-education/how-to-create-a-blockchain-in-python/

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.prev = None
        #TODO to add hash function that uses a merkle tree
        self.hash = ""

    #computes the hash for a block using sha256    
    def hash(self):
        if self.previous_hash == '0':
            string = json.dumps(self.__dict__, sort_keys = True)
            return sha256(string.encode()).hexdigest()
        else:
            pass

#Blockchain for the network
class BlockChain:
    def __init__(self):
        self.unconfirmed = None
        self.chain = None
        self.create_genesis_block()
        

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0" )
        genesis_block.hash = genesis_block.hash()
        self.chain = genesis_block

    def last_block(self):
        return self.chain

    def first_block(self):
        cur = self.chain
        while cur.prev!=None:
            cur = cur.prev
        return cur

    

    def add_block(self, nextblock, proof):
        previous_hash = self.last_block.hash
        if previous_hash!=nextblock.previous_hash:
            return False
        
        if not self.is_valid_proof(nextblock, proof):
            return False
        
        nextblock.hash = proof
        nextblock.prev = self.last_block
        chain = nextblock

        

    def is_valid_proof(self, currentblock, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == currentblock.compute_hash())






