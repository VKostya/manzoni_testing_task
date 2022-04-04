import os
from tokenize import Token
from fastapi import APIRouter, Body
from api.scripts import *
from db.db_scripts import *
from schemas.forms import TokenForm, TokenInDB
from db.models import *
from config import Settings as ST

router = APIRouter()


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
        contract_txn, private_key=ST.PRIVATE_KEY
    )
    web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_hash = web3.toHex(web3.keccak(signed_txn.rawTransaction))
    add_tx_hash_to_token(unique_hash, tx_hash)
    token = get_token_from_unique_hash(unique_hash)
    result = TokenInDB.from_orm(token)
    return result


@router.get("/list", name="list db items")
def list():
    with db_session:
        tokens = Token.select()
        result = [TokenInDB.from_orm(t) for t in tokens]
    return result


@router.get("/total_supply", name="get contract's total supply info")
def total_supply():
    try:
        web3 = get_web3()
        contract = web3.eth.contract(address=ST.CONTRACT_ADDRESS, abi=ST.ABI)
        response_json = {
            "contract_name": contract.functions.name().call(),
            "total_supply": contract.functions.totalSupply().call(),
        }
        return response_json
    except web3.exceptions.BadFunctionCallOutput as e:
        return {"result": e.message}
