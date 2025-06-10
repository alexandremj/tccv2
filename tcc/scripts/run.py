from scripts.deploy import compile_contract
from core.blockchain import w3

abi, bytecode = compile_contract()

w3 = w3()
account = w3.eth.accounts[0]
w3.eth.default_account = account

TestContract = w3.eth.contract(abi=abi, bytecode=bytecode)
creator_id = "1"
content = "Hello, Blockchain!"
active = True

# creator_id_bytes = w3.to_bytes(text=creator_id).ljust(32, b'\0')
# content_bytes = w3.to_bytes(text=content).ljust(32, b'\0')

# tx_hash = TestContract.constructor(creator_id_bytes, content_bytes, active).transact()
tx_hash = TestContract.constructor(creator_id, content).transact()

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("✅ Contract deployed at:", tx_receipt.contractAddress)

contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
breakpoint()
print("Create post")
tx_hash = contract.functions.createPost(creator_id, content).transact()
print("Returned hash:", tx_hash)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
post_id = contract.events.PostCreated().process_receipt(receipt)[0]['args']['postId']
breakpoint()
# print("Initial value:", contract.functions.getContent().call())
# contract.functions.setContent("Goodbye, cruel world").transact()
# print("Updated value:", contract.functions.getContent().call())
