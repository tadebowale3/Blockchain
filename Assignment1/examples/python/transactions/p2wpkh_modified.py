#!/usr/bin/env python3

"""
Example of a Pay-to-Witness-Pubkey-Hash (P2WPKH) transaction.
"""

import os, sys

# sys.path.append(os.path.dirname(__file__).split('/transactions')[0])
transaction_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(transaction_directory))
sys.path.append(os.path.dirname(transaction_directory + "../lib."))


from lib.encoder import encode_tx, encode_script
from lib.hash    import hash256
from lib.helper  import decode_address, hash_script, get_txid
from lib.sign    import sign_tx
from lib.rpc     import RpcSocket

## Setup our RPC socket.
rpc = RpcSocket({ 'wallet': 'TestnetWallet' })
assert rpc.check()

## First, we will lookup an existing utxo,
## and use that to fund our transaction.
test_utxo = rpc.get_utxo(0)

## Get a change address for TestnetWallet.
test_change_txout     = rpc.get_recv()
_, test_redeem_script = decode_address(test_change_txout['address'])

## Get a payment address for TestnetWallet2.
test2_rpc = RpcSocket({ 'wallet': 'TestnetWallet2' })
test2_payment_txout    = test2_rpc.get_recv()
_, test2_redeem_script = decode_address(test2_payment_txout['address'])

## Calculate our output amounts.
fee = 1000
test2_recv_value = test_utxo['value'] // 2
test_change_value = test_utxo['value'] // 2 - fee

## The initial spending transaction. This tx spends a previous utxo,
## and commits the funds to our P2WPKH transaction.

## The spending transaction.
atob_tx = {
    'version': 1,
    'vin': [{
        # We are unlocking the utxo from Alice.
        'txid': test_utxo['txid'],
        'vout': test_utxo['vout'],
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [
        {
            'value': test2_recv_value,
            'script_pubkey': [0, test2_redeem_script]
        },
        {
            'value': test_change_value,
            'script_pubkey': [0, test_redeem_script]
        }
    ],
    'locktime': 0
}

## Serialize the transaction and calculate the TXID.
atob_hex  = encode_tx(atob_tx)
atob_txid = hash256(bytes.fromhex(atob_hex))[::-1].hex()

## The redeem script is a basic Pay-to-Pubkey-Hash template.
redeem_script = f"76a914{test_utxo['pubkey_hash']}88ac"

## We are signing Alice's UTXO using BIP143 standard.
test_signature = sign_tx(
    atob_tx,                # The transaction.
    0,                      # The input being signed.
    test_utxo['value'],    # The value of the utxo being spent.
    redeem_script,          # The redeem script to unlock the utxo. 
    test_utxo['priv_key']  # The private key to the utxo pubkey hash.
)

## Include the arguments needed to unlock the redeem script.
atob_tx['vin'][0]['witness'] = [ test_signature, test_utxo['pub_key'] ]

print(f'''
## Pay-to-Witness-Pubkey-Hash Example ##

-- Transaction Id --
{atob_txid}

-- Test UTXO --
     Txid : {test_utxo['txid']}
     Vout : {test_utxo['vout']}
    Value : {test_utxo['value']}
     Hash : {test_utxo['pubkey_hash']}

-- Sending to Test2 --
  Address : {test2_payment_txout['address']}
    Coins : {test2_recv_value}

-- Change --
  Address : {test_change_txout['address']}
      Fee : {fee}
    Coins : {test_change_value}

-- Hex --
{encode_tx(atob_tx)}
''')