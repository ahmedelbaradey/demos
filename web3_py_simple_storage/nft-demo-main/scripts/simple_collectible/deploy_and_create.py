from scripts.generate import (
    CreateAllNFTImages,
    AddTokenID,
    GenerateMetadataForAllTraits,
    CombineNFTLayers,
    PublishNFT,
    pinFileToIPFS
)
import json
from brownie import SimpleCollectible
from scripts.helpful_scripts import get_account, OPENSEA_URL
import sys

print(sys.executable)


def deploy_and_create():

    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    CreateAllNFTImages()
    AddTokenID()
    GenerateMetadataForAllTraits()
    CombineNFTLayers()
    f = open(
        "./metadata/all-traits.json",
    )
    data = json.load(f)
    for i in data:
        token_id = i["tokenId"]
        PublishNFT(i)
        IMAGES_BASE_URI = "https://ipfs.io/ipfs/"
        sample_token_uri = IMAGES_BASE_URI + \
            pinFileToIPFS(token_id) + "?filename=" + str(token_id) + ".json"
        tx = simple_collectible.createCollectible(
            sample_token_uri, {"from": account})
        tx.wait(1)
        print(
            f"Awesome, you can view your NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}"
        )
        print("Please wait up to 20 minutes, and hit the refresh metadata button. ")
        ####
    f.close()
    return simple_collectible


def main():
    deploy_and_create()
