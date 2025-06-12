from web3 import Web3

from models.post import PostModel, PostUserContent
from scripts.deploy import compile_contract

BLOCKCHAIN_URL = "http://127.0.0.1:8545"


def w3():
    w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
    return w3


class BlockchainPostContract:
    def __init__(self, abi, bytecode):
        self.w3 = w3()
        self.contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = self.contract.constructor().transact()
        self.tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        self.deployed_contract = self.w3.eth.contract(
            address=self.tx_receipt.contractAddress, abi=abi
        )

    def create_post(self, post: PostUserContent) -> int:
        tx_hash = self.deployed_contract.functions.createPost(post.user, post.content).transact()
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return self.deployed_contract.events.PostCreated().process_receipt(receipt)[0]["args"][
            "postId"
        ]

    def get_post_by_id(self, post_id: str) -> PostModel:
        post_data = self.deployed_contract.functions.getPost(int(post_id)).call()
        return PostModel(
            id=post_id, user=post_data[0], content=post_data[1], active=post_data[2]
        )
    
    # todo[alexandremj]: continue from here, implementing update and delete


class _BlockchainRepository:
    def __init__(self):
        self.w3 = w3()
        if not self.w3.is_connected():
            raise ConnectionError(
                "Failed to connect to the blockchain at {}".format(BLOCKCHAIN_URL)
            )

        self.posts = BlockchainPostContract(*compile_contract())

# singleton quick implementation
BlockchainRepository = _BlockchainRepository()
