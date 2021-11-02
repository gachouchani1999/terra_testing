import base64
from terra_sdk.client.lcd import LCDClient
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.core.wasm import MsgStoreCode, MsgInstantiateContract, MsgExecuteContract, msgs
from terra_sdk.core.auth.data.tx import StdFee



terra = LCDClient(chain_id='bombay-12', url = "https://lcd.terra.dev")
contract = './cw721_base.wasm'


mk = MnemonicKey()
print(mk)
wallet1 = terra.wallet(mk)

contract_file = open(contract,'rb')
file_bytes = base64.b64encode(contract_file.read()).decode()
store_code = MsgStoreCode(wallet1.key.acc_address, file_bytes)
store_code_tx = wallet1.create_and_sign_tx(
    msgs = [store_code],
    gas_adjustment= 1.5,
)

store_code_tx_result = terra.tx.broadcast(store_code_tx)
print(store_code_tx_result)

code_id = store_code_tx_result.logs[0].events_by_type['store_code']['code_id'][0]
instantiate = MsgInstantiateContract(
    wallet1.key.acc_address,
    code_id,
    {'minter': wallet1.key.acc_address},
    {'name' : 'God NFT'},
    {'symbol': 'GNF'}

)

instantiate_tx = wallet1.create_and_sign_tx(
    msgs=[instantiate]
)

instantiate_tx_result = terra.tx.broadcast(instantiate_tx)
print(instantiate_tx_result)

contract_address = instantiate_tx_result.logs[0].events_by_type['instantiate_contract']['contract_address'][0]

execute = MsgExecuteContract(
    wallet1.key.acc_address,
    contract_address,
    {'mint': {}}
)


execute_tx = wallet1.create_and_sign_tx(
    msgs=[execute], fee=StdFee(1000000, Coins(uluna=1000000))
)

execute_tx_result = terra.tx.broadcast(execute_tx)
print(execute_tx_result)


result = terra.wasm.contract_query(contract_address, {"num_tokens": {}})
print(result)

