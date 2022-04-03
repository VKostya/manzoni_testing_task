# MANZONI TEST APP
## TO_DO

Here is a list of tasks that are needed to be done

### Create a DB Model

Token Model should contain these fields

- id - primary key
- unique_hash - Token's unique hash
- tx_hash - Transaction hash
- media_url - URL for an image
- owner - Owner's Address in ETH Network

I have chosen pony orm and created a sqlite database. I also added two functions that would be called in /tokens/create handler later

### Create views

The next views are needed to be designed

### /tokens/create

This view has next logic:

- get data from request body
- create unique_hash string using secrets.choise function
- initialize contract instance using web3 library (it is also used in /tokens/total_supply)
- sign the transaction and send it to Rinkeby Testnet Network
- save data

The responce looks like this:

{
  "id": 1,
  "unique_hash": "xxxxx11111XXXXX22222",
  "tx_hash": "0x...",
  "media_url": "url_from_request_body.jpg",
  "owner": "owners_eth_address"
}

### /tokens/list

This view responces with Token model list from db. 

The responce looks like:

[
    {
        "id": 1,
        "unique_hash": "xxxxx11111XXXXX22222",
        "tx_hash": "0x...",
        "media_url": "url_from_request_body.jpg",
        "owner": "owners_eth_address"
    },
    {
        "id": 2,
        "unique_hash": "xxxxx11111XXXXX22222",
        "tx_hash": "0x...",
        "media_url": "url_from_request_body.jpg",
        "owner": "owners_eth_address"
    }
    ...
]

### /tokens/total_supply

This view gives information about specific [smart contract](https://rinkeby.etherscan.io/address/0x92e098def0ca9577bd50ca61b90b9a46ec1f2040)

The responce contains these fields:
- contract_name - the name of a smart contract. I get this information using name() function
- total_supply -  the amount of tokens in existence. I get this information using totalSupply() function

The responce looks like this: 
{
    "contract_name": "some name",
    "total_supply": 100
}