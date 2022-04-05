from fastapi import APIRouter, Body
from pony.orm import db_session
from web3.exceptions import BadFunctionCallOutput

from app.db.db_scripts import (
    add_token,
    add_tx_hash_to_token,
    get_token_from_unique_hash,
)
from app.db.models import Token
from app.main import config
from app.schemas.forms import TokenForm, TokenInDB
from app.utils.transactions import get_unique_hash, get_web3, build_transaction

router = APIRouter()


@router.post("/create", name="token:create")
def create_token(token_form: TokenForm = Body(..., embed=True)):
    unique_hash = get_unique_hash()
    web3 = get_web3()

    add_token(unique_hash, token_form.media_url, token_form.owner)

    try:
        contract_txn = build_transaction(
            web3, token_form.owner, token_form.media_url, unique_hash
        )
    except ValueError as e:

        return {"error": e}

    signed_txn = web3.eth.account.sign_transaction(
        contract_txn, private_key=Config.PRIVATE_KEY
    )
    web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_hash = web3.toHex(web3.keccak(signed_txn.rawTransaction))
    add_tx_hash_to_token(unique_hash, tx_hash)
    token = get_token_from_unique_hash(unique_hash)

    return TokenInDB.from_orm(token)


@router.get("/list", name="token:list")
def get_tokens():
    with db_session:
        tokens = Token.select()
        result = [TokenInDB.from_orm(t) for t in tokens]

    return result


@router.get("/total_supply", name="get contract's total supply info")
def get_total_supply_info():
    try:
        web3 = get_web3()
        contract = web3.eth.contract(address=Config.CONTRACT_ADDRESS, abi=Config.ABI)
        return {
            "contract_name": contract.functions.name().call(),
            "total_supply": contract.functions.totalSupply().call(),
        }

    except BadFunctionCallOutput as e:
        return {"result": e}
