import os
from fastapi import APIRouter
from web3 import Web3


router = APIRouter()

def get_web3():
    infura_url = os.getenv("ENDPOINT")
    web3 = Web3(Web3.HTTPProvider(infura_url))
    return web3

@router.get('/total_supply')
def total_supply():
    try:
        web3 = get_web3()
        contract = web3.eth.contract(address=os.getenv("CONTRACT_ADDRESS"), abi=os.getenv("ABI"))
        response_json = {"contract_name": 
                            contract.functions.name().call(),
                        "total_supply": 
                            contract.functions.totalSupply().call()
                    }
        return response_json
    except web3.exceptions.BadFunctionCallOutput as e:
        return {"result": e.message}
    