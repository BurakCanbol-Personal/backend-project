from flask import Blueprint, request, jsonify, abort
from app.utils.data_handler import load_datasets
from app.utils.data_handler import save_datasets
from app.services.auth_service import has_permission
from app.utils.logger import log_event
from app.utils.data_handler import get_dataset_by_id
from datetime import datetime


datasets_bp = Blueprint("datasets", __name__)

@datasets_bp.route("/datasets", methods=["GET"])
def get_datasets():
    datasets = load_datasets()
    return jsonify(datasets)



@datasets_bp.route("/datasets", methods=["POST"])
def add_dataset():
    role = request.headers.get("Role", "student")
    
    if not has_permission(role, "upload"):
        log_event(
            event_name="dataset_upload_denied",
            level="warning",
            status="failed",
            details={
                "role": role,
                "action": "upload"
            }
        )
        abort(403, description="Access denied")
    
    
    request_data = request.get_json()
    if request_data is None:
        log_event(
            event_name="invalid_request",
            level="warning",
            status="failed",
            details={
                "role": role,
                "reason":"invalid_json"
            }
        )
        
        abort(400, description="Request body must be valid JSON")
        
        
    name = request_data.get("name")
    if name is None or not name.strip():
        log_event(
            event_name="invalid_request",
            level="warning",
            status="failed",
            details={
                "role": role,
                "reason":"missing_name"
            }
        )
        abort(400, description="Dataset name is required")
    
    datasets = load_datasets()
    
    new_dataset = {
        "id": len(datasets) + 1,
        "name": name.strip(),
        "uploaded_by": role,
        "status": "raw",
        "created_at": datetime.now().isoformat()
    }
    
    datasets.append(new_dataset)
    save_datasets(datasets)
    
    log_event(
        event_name="dataset_uploaded",
        status="success",
        level="info",
        details={
            "role": role,
            "dataset_id": new_dataset["id"],
            "dataset_name": new_dataset["name"],
            "created_at": new_dataset["created_at"]
        }
    )
    
    
    
    return jsonify(new_dataset), 201
    
    
@datasets_bp.route("/datasets/<dataset_id>", methods=["GET"])
def get_dataset(dataset_id):
    dataset = get_dataset_by_id(dataset_id)
    
    role = request.headers.get("Role", "student")
    
    if dataset is None:
        log_event(
            event_name="dataset_lookup_failed",
            level="warning",
            status="failed",
            details={
                "dataset_id": dataset_id,
                "role": role,
                "action": "get_dataset",
                "reason": "missing_dataset"
            }
        )
        abort(404, description="Dataset not found")
        
    return jsonify(dataset)
        