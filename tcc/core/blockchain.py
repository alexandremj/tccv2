from datetime import datetime
from uuid import uuid4

from web3 import Web3

from models.post import PostContentVersions, PostModel, PostUserContent
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

    def create_post(self, post: PostUserContent) -> str:
        post_id = str(uuid4())
        tx_hash = self.deployed_contract.functions.createPost(
            post_id, post.user, post.content
        ).transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return self.get_post_by_id(post_id)

    def get_post_by_id(self, post_id: str) -> PostContentVersions:
        posts = self.deployed_contract.functions.getPost(post_id).call()
        parsed_posts = [self._build_model_from_blockchain_post(post) for post in posts]
        return PostContentVersions(current=parsed_posts[-1], previous=parsed_posts[:-1])

    def _build_model_from_blockchain_post(self, post: tuple) -> PostModel:
        date_format = "%Y-%m-%d %H:%M:%S"
        return PostModel(
            identifier=str(post[0]),
            user=post[1],
            content=post[2],
            active=post[3],
            creation_time=datetime.fromtimestamp(post[4]).strftime(date_format),
            update_time=datetime.fromtimestamp(post[5]).strftime(date_format),
        )

    def get_all_posts(self) -> list[PostModel]:
        posts = self.deployed_contract.functions.getPosts().call()
        return [self._build_model_from_blockchain_post(post) for post in posts]

    def update_post_content(self, post_id: str, content: str) -> PostModel:
        tx_hash = self.deployed_contract.functions.setPostContent(
            post_id, content
        ).transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return self.get_post_by_id(post_id)


class BlockchainRepository:
    _instance = None

    def __init__(self):
        self.w3 = w3()
        if not self.w3.is_connected():
            raise ConnectionError(
                "Failed to connect to the blockchain at {}".format(BLOCKCHAIN_URL)
            )

        self.posts = BlockchainPostContract(*compile_contract())

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
