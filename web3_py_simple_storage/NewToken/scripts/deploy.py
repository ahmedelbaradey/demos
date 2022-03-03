from pickle import TRUE
from brownie import ITRN
from scripts.helpful_scripts import get_account
from web3 import Web3

initial_supply = Web3.toWei(1000, "ether")


def main():
    account = get_account()
    our_token = ITRN.deploy(initial_supply, {"from": account}, publish_source=TRUE)
    print(our_token.name())
