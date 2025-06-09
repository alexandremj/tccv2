# todo: clean this, more of a script than actual application code

import json

from web3 import Web3
from solcx import compile_standard, install_solc

install_solc('0.8.0')


with open("./contracts/test.sol", "r") as f:
    test_contract = f.read()


compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "MyContract.sol": {
            "content": test_contract
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
}, solc_version="0.8.0")

with open("./compiled_code.json","w") as file:
    json.dump(compiled_sol,file)

contract_name = "MyContract"
abi = compiled_sol["contracts"][f'{contract_name}.sol'][contract_name]['abi']
bytecode = compiled_sol['contracts'][f'{contract_name}.sol'][contract_name]['evm']['bytecode']['object']

print("✅ Compilation successful")
print("ABI:", json.dumps(abi, indent=2))
print("Bytecode:", bytecode[:60] + "...")

# todo: change to environment variable
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
account = w3.eth.accounts[0]
w3.eth.default_account = account

TestContract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = TestContract.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("✅ Contract deployed at:", tx_receipt.contractAddress)

contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
breakpoint()
print("Initial value:", contract.functions.getValue().call())

