from pyteal import *


def approval_program():

    tmpl_fee = Int(1000)
    tmpl_period = Int(50)
    tmpl_dur = Int(5000)
    tmpl_x = Bytes("base64", "023sdDE2")
    tmpl_amt = Int(2000)
    tmpl_rcv = Addr("6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY")
    tmpl_timeout = Int(30000)

    periodic_pay_core = And(Txn.type_enum() == Int(1),
                            Txn.fee() < tmpl_fee,
                            Txn.first_valid() % tmpl_period == Int(0),
                            Txn.last_valid() == tmpl_dur + Txn.first_valid(),
                            Txn.lease() == tmpl_x)

    periodic_pay_transfer = And(Txn.close_remainder_to() ==  Global.zero_address(),
                                Txn.receiver() == tmpl_rcv,
                                Txn.amount() == tmpl_amt)

    periodic_pay_close = And(Txn.close_remainder_to() == tmpl_rcv,
                             Txn.receiver() == Global.zero_address(),
                             Txn.first_valid() == tmpl_timeout,
                             Txn.amount() == Int(0))

    periodic_pay_escrow = periodic_pay_core.And(periodic_pay_transfer.Or(periodic_pay_close))

    # Mode.Application specifies that this is a smart contract
    return compileTeal(periodic_pay_escrow, Mode.Application, version=4)


def clear_state_program():
    program = Return(Int(1))

    # Mode.Application specifies that this is a smart contract
    return compileTeal(program, Mode.Application, version=4)


# print out the results
print(approval_program())
print(clear_state_program())
