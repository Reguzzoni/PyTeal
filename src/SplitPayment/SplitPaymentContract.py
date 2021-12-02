from pyteal import *

"""Split Payment"""

def approval_program():
    tmpl_fee = Int(1000)
    tmpl_rcv1 = Addr("RSDIDU3W2OIIKVE6HTW2NBSEKNVSVCNLCZ6M4KUII7ZTBF7PL74DSJWWXU")
    tmpl_rcv2 = Addr("F4FXONSP6GWF2M7I3JL5LOM2LTVUC3Z5QM6TM26EVART7TQZ7PK5NBH2WY")
    tmpl_own = Addr("5SDQLV6KOEGAMUXU3TO5UE5Y7ZAAX7IMD4D337IXYBOIE3HW73LT7DPQMY")
    tmpl_ratn = Int(1)
    tmpl_ratd = Int(3)
    tmpl_min_pay = Int(1000)
    tmpl_timeout = Int(3000)

    split_core = And(
        Txn.type_enum() == TxnType.Payment,
        Txn.fee() < tmpl_fee,
        Txn.rekey_to() == Global.zero_address(),
        )

    split_transfer = And(
        Gtxn[0].sender() == Gtxn[1].sender(),
        Txn.close_remainder_to() == Global.zero_address(),
        Gtxn[0].receiver() == tmpl_rcv1,
        Gtxn[1].receiver() == tmpl_rcv2,
        Gtxn[0].amount()
        == ((Gtxn[0].amount() + Gtxn[1].amount()) * tmpl_ratn) / tmpl_ratd,
        Gtxn[0].amount() == tmpl_min_pay,
        )

    split_close = And(
        Txn.close_remainder_to() == tmpl_own,
        Txn.receiver() == Global.zero_address(),
        Txn.amount() == Int(0),
        Txn.first_valid() > tmpl_timeout,
        )

    split_program = And(
        split_core, If(Global.group_size() == Int(2), split_transfer, split_close)
    )

    # Mode.Application specifies that this is a smart contract
    return compileTeal(split_program, Mode.Application, version=2)


def clear_state_program():
    program = Return(Int(1))

    # Mode.Application specifies that this is a smart contract
    return compileTeal(program, Mode.Application, version=2)


if __name__ == "__main__":
    print(approval_program())
