
creatures = {
    "singleCell": {
        "id": "singleCell",
        "name": "Single Cell",
        "type": "Organism",
        "maxhp": 35,
        "speed": 3,
        "attack": 1,
        "foodToUpgrade": 15,
        "stageToEvolve": 15,
        "imageName": "SingleCellOrganism"
    },
    "multiCell": {
        "id": "multiCell",
        "name": "Multi Cell",
        "type": "Organism",
        "maxhp": 45,
        "speed": 3.5,
        "attack": 5,
        "foodToUpgrade": 20,
        "stageToEvolve": 15,
        "imageName": "MultiCellOrganism"
    },
    "bacteriaProkaryotes": {
        "id": "bacteriaProkaryotes",
        "name": "Prokaryotes",
        "type": "Bacteria",
        "maxhp": 50,
        "speed": 4.5,
        "attack": 10,
        "foodToUpgrade": 20,
        "stageToEvolve": 15,
        "imageName": "ProkaryotesBacteria"
    }
}

tiers = {
    1: "singleCell",
    2: "multiCell",
    3: "bacteriaProkaryotes"
}


def getTiers():
    return tiers


def getCreatures():
    return creatures
