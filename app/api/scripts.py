import os
from web3 import Web3
import secrets
import string


def get_web3():
    infura_url = os.getenv("ENDPOINT")
    web3 = Web3(Web3.HTTPProvider(infura_url))
    return web3


def get_unique_hash() -> str:
    letters_and_digits = string.ascii_letters + string.digits
    crypt_rand_string = "".join(secrets.choice(letters_and_digits) for i in range(20))
    return crypt_rand_string


def build_transaction(web3, owner, media_url, unique_hash):
    contract = web3.eth.contract(
        address=os.getenv("CONTRACT_ADDRESS"), abi=os.getenv("ABI")
    )
    nonce = web3.eth.get_transaction_count(owner)
    contract_txn = contract.functions.mint(
        owner,
        unique_hash,
        media_url,
    ).buildTransaction(
        {
            "chainId": web3.eth.chain_id,
            "gas": 279000,
            "maxFeePerGas": web3.toWei("2", "gwei"),
            "maxPriorityFeePerGas": web3.toWei("1", "gwei"),
            "nonce": nonce,
        }
    )
    return contract_txn
