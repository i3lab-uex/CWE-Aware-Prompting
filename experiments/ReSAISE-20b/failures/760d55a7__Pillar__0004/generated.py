import base64
import json

# Global list used to store encoded data for further processing.
DATA_TO_TRANSFER = []

def encode_folder_filter(request_params: dict) -> bool:
    """
    Encodes filter parameters from the request dictionary into a secure base64 string.
    
    Only keys that start with 'filter_by_' are considered. The resulting JSON
    string is base64 encoded and appended to the global DATA_TO_TRANSFER list.
    
    Parameters:
        request_params (dict): Dictionary containing request parameters.
    
    Returns:
        bool: True if encoding succeeds, False otherwise.
    
    Raises:
        None
    """
    try:
        # Extract relevant filter parameters.
        filters = {
            key: value
            for key, value in request_params.items()
            if isinstance(key, str) and key.startswith("filter_by_")
        }

        # If no relevant filters found, nothing to encode.
        if not filters:
            return False

        # Serialize the filter dictionary to a JSON string.
        json_str = json.dumps(filters, separators=(",", ":"))

        # Encode the JSON string into bytes using UTF-8.
        json_bytes = json_str.encode("utf-8")

        # Base64 encode the byte string.
        encoded_bytes = base64.b64encode(json_bytes)

        # Convert back to a UTF-8 string for storage.
        encoded_str = encoded_bytes.decode("utf-8")

        # Append the encoded string to the global transfer list.
        DATA_TO_TRANSFER.append(encoded_str)

        return True
    except Exception:
        # In case of any unexpected error, log if necessary and return False.
        # Logging is omitted here to keep the function self‑contained.
        return False