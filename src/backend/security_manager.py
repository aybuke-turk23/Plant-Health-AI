import os
import time

# To track the last request time (Rate Limiting)
last_request_time = 0

def validate_input(image_path):
    """
    Input Validation: Checks file type and size.
    """
    # 1. File Type Check
    allowed_extensions = ['.jpg', '.jpeg', '.png']
    extension = os.path.splitext(image_path)[1].lower()
    
    if extension not in allowed_extensions:
        return False, f"Error: {extension} extension is not allowed. Only JPG and PNG are accepted!"

    # 2. File Size Limit (Maximum 5MB)
    try:
        file_size = os.path.getsize(image_path) / (1024 * 1024) # Convert to MB
        if file_size > 5:
            return False, f"Error: File is too large ({file_size:.2f}MB). Limit is 5MB!"
    except FileNotFoundError:
        return False, "Error: File not found!"
        
    return True, "Valid"

def check_rate_limit():
    """
    Rate Limiting: Enforces a 10-second delay between requests.
    """
    global last_request_time
    current_time = time.time()
    cooldown = 10 # seconds
    
    if current_time - last_request_time < cooldown:
        remaining = int(cooldown - (current_time - last_request_time))
        return False, f"Error: Too many requests! Please wait {remaining} seconds."
    
    last_request_time = current_time
    return True, "Request allowed"