from web3 import Web3
import secrets
import string

from ..config import config


def get_web3():
    return Web3(Web3.HTTPProvider(config.ENDPOINT))


def get_unique_hash():
    letters_and_digits = string.ascii_letters + string.digits
    return "".join(secrets.choice(letters_and_digits) for _ in range(20))


def build_transaction(web3, owner, media_url, unique_hash):
    contract = web3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.ABI)
    nonce = web3.eth.get_transaction_count(owner)

    return contract.functions.mint(owner, unique_hash, media_url).buildTransaction(
        {
            "chainId": web3.eth.chain_id,
            "gas": 279000,
            "maxFeePerGas": web3.toWei("2", "gwei"),
            "maxPriorityFeePerGas": web3.toWei("1", "gwei"),
            "nonce": nonce,
        }
    )
