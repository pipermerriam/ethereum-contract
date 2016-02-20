Contracts
=========


* ``eth_contract.Contract(contract_meta, contract_name):``

This function returns a python class for the provided contract data.  It will
have functions for each of the defined functions in the provided contract ABI.


The Contract Class
------------------

* ``ContractClass(address, blockchain_client)``

The python class returned from ``eth_contract.Contract`` takes an ethereum
address and a blockchain client as constructor arguments.  This returns an
instance of your contract that can be used to interact with the contract via
the provided ``blockchain_client``


* ``ContractClass.get_deploy_data(*constructor_args)``

This *classmethod* will return the hex encoded data for deploying this
contract.


* ``ContractClass._meta.code``

The compiled contract code.


* ``ContractClass._meta.source``

The contract source code.


* ``ContractClass._meta.blockchain_client``

The blockchain client this contract will use to interact with the blockchain.


* ``ContractClass._meta.abi``

The contract ABI.


* ``ContractClass.get_balance(block="latest")``

Returns contract balance in wei as an integer.


Contract Functions
------------------

For each function defined in the contract ABI there will be a callable property
by the same name on the contract object.  Each of these functions accepts the
following additional keyword arguments in addition to the function arguments.

* ``value`` - sends the provided value in wei with the transaction.
* ``_from`` - the ethereum address that the transaction should be sent from.
* ``gas`` - specifies the gas value of the transaction.
* ``gas_price`` - the gas price for the transaction.

Functions which are denoted as ``constant`` will not send transactions when
called and will return the return value of the called contract function.

Non-constant functions will send a transaction when called and will return the
transaction hash of the created transaction.
