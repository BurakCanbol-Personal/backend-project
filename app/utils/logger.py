import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def log_event(event_name, level="info", status=None, details=None):
    message = (f"event={event_name}")
    if status is not None:
        message = message + (f" status={status}")
        
    if details is not None:
        for key, value in details.items():
            message = message + (f" {key}={value}")
        
    if level == "info":
        logging.info(message)
    
    elif level == "warning":
        logging.warning(message)
        
    elif level == "error":
        logging.error(message)
        
    else:
        logging.info(message)