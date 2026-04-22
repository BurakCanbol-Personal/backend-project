import os
import json

DATA_PATH = "data/datasets.json"

def load_datasets():
    if not os.path.exists(DATA_PATH):
        return []
    
    with open(DATA_PATH, "r") as file:
        return json.load(file)


def save_datasets(data):
    with open(DATA_PATH, "w") as file:
        json.dump(data, file, indent=4)
        

def get_dataset_by_id(dataset_id):
    datasets = load_datasets()
    
    try:
        dataset_id_int = int(dataset_id)
    except ValueError:
        return None
    
    for dataset in datasets:
        if dataset["id"] == dataset_id_int:
            return dataset
    
    return None
    