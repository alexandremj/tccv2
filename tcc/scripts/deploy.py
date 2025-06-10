# todo: clean this, more of a script than actual application code

import json

from solcx import compile_standard, install_solc


install_solc('0.8.0')


def compile_contract():
    with open("./contracts/post.sol", "r") as f:
        test_contract = f.read()

    breakpoint()

    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "Chain.sol": {
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

    contract_name = "Chain"
    abi = compiled_sol["contracts"][f'{contract_name}.sol'][contract_name]['abi']
    bytecode = compiled_sol['contracts'][f'{contract_name}.sol'][contract_name]['evm']['bytecode']['object']

    print("✅ Compilation successful")
    print("ABI:", json.dumps(abi, indent=2))
    print("Bytecode:", bytecode[:60] + "...")
    return abi, bytecode

def deploy_contract(abi, bytecode):
    ...