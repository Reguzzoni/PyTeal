
from pyteal import *

"""Atomic Swap"""
alice = Addr("5SDQLV6KOEGAMUXU3TO5UE5Y7ZAAX7IMD4D337IXYBOIE3HW73LT7DPQMY")
bob = Addr("F4FXONSP6GWF2M7I3JL5LOM2LTVUC3Z5QM6TM26EVART7TQZ7PK5NBH2WY")
secret = Bytes("base32", "2323232323232323")
timeout = 3000

def htlc(
    tmpl_seller=alice,
    tmpl_buyer=bob,
    tmpl_fee=1000,
    tmpl_secret=secret,
    tmpl_hash_fn=Sha256,
    tmpl_timeout=timeout,
):
    fee_cond = Txn.fee() < Int(tmpl_fee)
    safety_cond = And(
        Txn.type_enum() == TxnType.Payment,
        Txn.close_remainder_to() == Global.zero_address(),
        Txn.rekey_to() == Global.zero_address(),
        )
    recv_cond = And(Txn.receiver() == tmpl_seller, tmpl_hash_fn(Arg(0)) == tmpl_secret)
    esc_cond = And(Txn.receiver() == tmpl_buyer, Txn.first_valid() > Int(tmpl_timeout))
    return And(fee_cond, safety_cond, Or(recv_cond, esc_cond))

if __name__ == "__main__":
    print(compileTeal(htlc(), mode=Mode.Signature, version=2))
