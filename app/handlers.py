import os
from fastapi import APIRouter, Body
from web3 import Web3
from forms import TokenForm
from models import add_token, add_tx_hash_to_token
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


@router.post("/create", name="token:create")
def create(token_form: TokenForm = Body(..., embed=True)):
    unique_hash = get_unique_hash()
    add_token(unique_hash, token_form.media_url, token_form.owner)
    return {"media_url": token_form.media_url, "owner": token_form.owner}


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
