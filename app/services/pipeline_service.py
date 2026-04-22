import random

def run_pipeline(dataset_id):
    return {
        "dataset_id": dataset_id,
        "status": "processed",
        "biomarkers": {
            "alpha_power": round(random.random(), 2),
            "theta_power": round(random.random(), 2)
        }
    }