import logging
import os

def setup_task_logger(task_name:str, log_dir:str) -> logging.Logger:
    try:
        # Create a logger
        logger = logging.getLogger(task_name)
        logger.setLevel(logging.DEBUG)  # Set the logging level

        # Create a file handler for the log file
        log_file = os.path.join(log_dir, f"{task_name}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)  # Set the logging level for the file handler

        # Create a console handler for the console output (optional)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Set the logging level for the console handler

        # Create a formatter and set it for the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    except Exception as e:
        raise ValueError(f"Error setting up task logger {log_dir} {task_name}: {e}")
    return logger