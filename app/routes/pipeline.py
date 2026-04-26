from flask import Blueprint, request, jsonify, abort
from app.utils.data_handler import get_dataset_by_id, load_datasets
from app.utils.data_handler import save_datasets
from app.services.auth_service import has_permission
from app.utils.logger import log_event
from app.services.pipeline_service import run_pipeline
from datetime import datetime


pipeline_bp = Blueprint("pipeline", __name__)

@pipeline_bp.route("/pipeline/run/<dataset_id>", methods=["POST"])
def run_pipeline_route(dataset_id):
    role = request.headers.get("Role", "student")
    
    if not has_permission(role, "run_pipeline"):
        log_event(
            event_name="pipeline_run_denied",
            level="warning",
            status="failed",
            details={
                "dataset_id": dataset_id,
                "role": role,
                "action": "run_pipeline"
            }
        )
        abort(403, description="Access denied")
    
    
    dataset = get_dataset_by_id(dataset_id)
    
    if dataset["status"] == "processed":
        log_event(
            event_name="pipeline_run_blocked",
            level="warning",
            status="failed",
            details={
                "dataset_id": dataset_id,
                "role": role,
                "reason": "already_processed"
            }
        )
        abort(409, description="Dataset already processed")
    
    
    if dataset is None:
        log_event(
            event_name="pipeline_run_failed",
            level="warning",
            status="failed",
            details={
                "dataset_id": dataset_id,
                "role": role,
                "action": "run_pipeline",
                "reason": "dataset_not_found"
            }
        )
        abort(404, description="Invalid dataset request")
    
    
    log_event(
        event_name="pipeline_started",
        level="info",
        status="started",
        details={
            "dataset_id": dataset_id,
            "role": role,
            "action": "run_pipeline"
        }
    )
    
    result = run_pipeline(dataset_id)
    dataset["status"] = "processed"
    dataset["results"] = result["biomarkers"]
    dataset["processed_at"] = datetime.now().isoformat()
    
    datasets = load_datasets()
    for i, d in enumerate(datasets):
        if d["id"] == dataset["id"]:
            datasets[i] = dataset
            break
        
    save_datasets(datasets)
    
    log_event(
        event_name="pipeline_run_completed",
        level="info",
        status="success",
        details={
            "dataset_id": dataset["id"],
            "dataset_name": dataset["name"],
            "role": role,
            "action": "run_pipeline",
            "processed_at": dataset["processed_at"]
        }
    )
    
    return jsonify(result)