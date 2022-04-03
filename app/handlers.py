from distutils.log import error
import os
from fastapi import APIRouter, Body
from web3 import Web3
from forms import TokenForm, TokenInDB
from models import add_token, add_tx_hash_to_token, get_token_from_unique_hash
import secrets
import string


router = APIRouter()


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


@router.post("/create", name="token:create")
def create(token_form: TokenForm = Body(..., embed=True)):
    unique_hash = get_unique_hash()
    add_token(unique_hash, token_form.media_url, token_form.owner)
    web3 = get_web3()
    contract_txn = ""
    try:
        contract_txn = build_transaction(
            web3, token_form.owner, token_form.media_url, unique_hash
        )
    except ValueError as e:
        return {"error": e["message"]}
    signed_txn = web3.eth.account.sign_transaction(
        contract_txn, private_key=os.getenv("PRIVATE_KEY")
    )
    web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_hash = web3.toHex(web3.keccak(signed_txn.rawTransaction))
    add_tx_hash_to_token(unique_hash, tx_hash)
    token = get_token_from_unique_hash(unique_hash)
    result = TokenInDB.from_orm(token)
    return result


@router.get("/total_supply")
def total_supply():
    try:
        web3 = get_web3()
        contract = web3.eth.contract(
            address=os.getenv("CONTRACT_ADDRESS"), abi=os.getenv("ABI")
        )
        response_json = {
            "contract_name": contract.functions.name().call(),
            "total_supply": contract.functions.totalSupply().call(),
        }
        return response_json
    except web3.exceptions.BadFunctionCallOutput as e:
        return {"result": e.message}
