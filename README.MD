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

### Create views

The next API is needed to be designed

### /tokens/create  

### /tokens/list

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