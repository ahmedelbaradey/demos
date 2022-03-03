import random
import json
# from IPython.display import display
import requests
from PIL import Image
from brownie import config
# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

background = ["Blue", "Orange", "Purple", "Red", "Yellow", "Green"]
background_weights = [30, 40, 15, 5, 10, 10]

body = ["Blue", "Orange", "Purple", "Red", "Yellow", "Green"]
body_weights = [30, 40, 15, 5, 10, 10]

fan = ["Blue", "Orange", "Purple", "Red", "Yellow", "Green"]
fan_weights = [30, 40, 15, 5, 10, 10]

planenose = ["Blue", "Orange", "Purple", "Red", "Yellow", "Green"]
planenose_weights = [30, 40, 15, 5, 10, 10]

tail = ["Blue", "Orange", "Purple", "Red", "Yellow", "Green"]
tail_weights = [30, 40, 15, 5, 10, 10]

wings = ["Blue", "Orange", "Purple", "Red", "Yellow", "Green"]
wings_weights = [30, 40, 15, 5, 10, 10]


# Dictionary variable for each trait.
# Eech trait corresponds to its file name

background_files = {
    "Blue": "blue",
    "Orange": "orange",
    "Purple": "purple",
    "Red": "red",
    "Yellow": "yellow",
    "Green": "green",
}

body_files = {
    "Blue": "blue",
    "Orange": "orange",
    "Purple": "purple",
    "Red": "red",
    "Yellow": "yellow",
    "Green": "green",
}

fan_files = {
    "Blue": "blue",
    "Orange": "orange",
    "Purple": "purple",
    "Red": "red",
    "Yellow": "yellow",
    "Green": "green",
}

planenose_files = {
    "Blue": "blue",
    "Orange": "orange",
    "Purple": "purple",
    "Red": "red",
    "Yellow": "yellow",
    "Green": "green",
}

tail_files = {
    "Blue": "blue",
    "Orange": "orange",
    "Purple": "purple",
    "Red": "red",
    "Yellow": "yellow",
    "Green": "green",
}
wings_files = {
    "Blue": "blue",
    "Orange": "orange",
    "Purple": "purple",
    "Red": "red",
    "Yellow": "yellow",
    "Green": "green",
}

# Generate Traits

TOTAL_IMAGES = 5  # Number of random unique images we want to generate
all_images = []

# A recursive function to generate unique image combinations


def create_new_image():
    new_image = {}  #
    # For each trait category, select a random trait based on the weightings
    new_image["Background"] = random.choices(background, background_weights)[0]
    new_image["Body"] = random.choices(body, body_weights)[0]
    new_image["Fan"] = random.choices(fan, fan_weights)[0]
    new_image["PlaneNose"] = random.choices(planenose, planenose_weights)[0]
    new_image["Tail"] = random.choices(tail, tail_weights)[0]
    new_image["Wings"] = random.choices(wings, wings_weights)[0]
    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


def CreateAllNFTImages():
    # Generate the unique combinations based on trait weightings
    for i in range(TOTAL_IMAGES):
        new_trait_image = create_new_image()
        all_images.append(new_trait_image)


def AddTokenID():
    i = 0
    for item in all_images:
        item["tokenId"] = i
        i = i + 1


def GenerateMetadataForAllTraits():
    # Generate Metadata for all Traits
    METADATA_FILE_NAME = "./metadata/all-traits.json"
    with open(METADATA_FILE_NAME, "w") as outfile:
        json.dump(all_images, outfile, indent=4)


def CombineNFTLayers():
    # Generate Images
    for item in all_images:
        im1 = Image.open(
            f'./trait-layers/background/{background_files[item["Background"]]}.png'
        ).convert("RGBA")
        im2 = Image.open(f'./trait-layers/body/{body_files[item["Body"]]}.png').convert(
            "RGBA"
        )
        im3 = Image.open(f'./trait-layers/tail/{tail_files[item["Tail"]]}.png').convert(
            "RGBA"
        )
        im4 = Image.open(f'./trait-layers/fan/{fan_files[item["Fan"]]}.png').convert(
            "RGBA"
        )
        im5 = Image.open(
            f'./trait-layers/wings/{wings_files[item["Wings"]]}.png'
        ).convert("RGBA")
        im6 = Image.open(
            f'./trait-layers/planenose/{planenose_files[item["PlaneNose"]]}.png'
        ).convert("RGBA")

        # Create each composite
        com1 = Image.alpha_composite(im1, im2)
        com2 = Image.alpha_composite(com1, im3)
        com3 = Image.alpha_composite(com2, im4)
        com4 = Image.alpha_composite(com3, im5)
        com5 = Image.alpha_composite(com4, im6)

        # Convert to RGB
        rgb_im = com5.convert("RGB")
        file_name = str(item["tokenId"]) + ".png"
        rgb_im.save("./images/" + file_name)
        print(f"{file_name}  Created")

    # Generate Metadata for each Image


def PublishNFT(_token):
    IMAGES_BASE_URI = "https://ipfs.io/ipfs/"
    PROJECT_NAME = "New NFT"
    token_id = _token["tokenId"]
    token = {
        "image": IMAGES_BASE_URI
        + pinImageToIPFS(token_id)
        + "?filename="
        + str(token_id)
        + ".png",
        "tokenId": token_id,
        "name": PROJECT_NAME + " " + str(token_id),
        "attributes": [],
    }
    token["attributes"].append(getAttribute(
        "Background", _token["Background"]))
    token["attributes"].append(getAttribute("Body", _token["Body"]))
    token["attributes"].append(getAttribute("Fan", _token["Fan"]))
    token["attributes"].append(getAttribute("Tail", _token["Tail"]))
    token["attributes"].append(getAttribute("Wings", _token["Wings"]))
    token["attributes"].append(getAttribute("PlaneNose", _token["PlaneNose"]))

    fileName = str(token_id) + ".json"
    print(f"{fileName} Created")
    with open("./metadata/" + fileName, "w") as outfile:
        json.dump(token, outfile, indent=4)


def pinImageToIPFS(TokenID):

    _files = [
        ("file", ("" + str(TokenID) + ".png",
         open("./images/" + str(TokenID) + ".png", "rb"))),
    ]
    headers = {
        "pinata_api_key": config["pinata"]["api_key"],
        "pinata_secret_api_key": config["pinata"]["api_secret"],
    }
    ipfs_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    response: requests.Response = requests.post(
        url=ipfs_url, files=_files, headers=headers
    )
    print(f"{TokenID} Image Uploaded")
    return response.json()["IpfsHash"]


def pinFileToIPFS(TokenID):
    _files = [
        (
            "file",
            ("" + str(TokenID) + ".json",
             open("./metadata/" + str(TokenID) + ".json", "rb")),
        ),
    ]
    headers = {
        "pinata_api_key": config["pinata"]["api_key"],
        "pinata_secret_api_key": config["pinata"]["api_secret"],
    }
    ipfs_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    response: requests.Response = requests.post(
        url=ipfs_url, files=_files, headers=headers
    )
    print(f"{TokenID} Metadata Uploaded")
    return response.json()["IpfsHash"]


def getAttribute(key, value):
    return {"trait_type": key, "value": value}


def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)
