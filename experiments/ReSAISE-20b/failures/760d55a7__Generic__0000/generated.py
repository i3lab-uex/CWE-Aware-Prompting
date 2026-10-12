import base64
import json

# List to hold encoded data for further processing.
DATA_TO_TRANSFER = []

def encode_folder_filter(request_params: dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a secure base64 string.
    
    Parameters
    ----------
    request_params : dict
        Dictionary representing the request parameters.

    Returns
    -------
    bool
        True if encoding was successful and data appended to DATA_TO_TRANSFER,
        False otherwise (e.g., no filter parameters found or an error occurred).
    """
    if not isinstance(request_params, dict):
        return False

    # Extract parameters whose keys start with 'filter_by_'
    filtered = {k: v for k, v in request_params.items() if k.startswith("filter_by_")}

    if not filtered:
        # Nothing to encode
        return False

    try:
        # Serialize the filtered dict into JSON string
        json_str = json.dumps(filtered, separators=(",", ":"))
        # Encode the JSON string into bytes and then to base64
        b64_bytes = base64.urlsafe_b64encode(json_str.encode("utf-8"))
        # Store as a decoded string for readability (optional)
        DATA_TO_TRANSFER.append(b64_bytes.decode("utf-8"))
    except Exception:
        # Any error (serialization, encoding) results in False
        return False

    return True