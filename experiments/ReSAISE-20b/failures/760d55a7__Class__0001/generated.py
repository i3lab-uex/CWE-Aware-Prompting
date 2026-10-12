import base64
import json
from typing import Dict, Any

# Global list to store the encoded data for further processing
DATA_TO_TRANSFER: list[str] = []

# Maximum allowed size of the JSON string (in bytes) to avoid uncontrolled resource consumption
MAX_JSON_SIZE_BYTES = 1_048_576  # 1 MiB

def encode_folder_filter(request_params: Dict[str, Any]) -> bool:
    """
    Encode filter parameters from the request dictionary into a secure base64 string.
    
    Parameters
    ----------
    request_params : dict
        A dictionary representing the request parameters.

    Returns
    -------
    bool
        True if the encoding is successful, False otherwise.
    """
    try:
        # Extract only keys that start with 'filter_by_'
        filter_dict = {k: v for k, v in request_params.items() if isinstance(k, str) and k.startswith("filter_by_")}

        # If no filter parameters were found, nothing to encode
        if not filter_dict:
            return False

        # Serialize the dictionary to a JSON string
        json_str = json.dumps(filter_dict, separators=(",", ":"))

        # Guard against uncontrolled resource consumption by limiting the size
        if len(json_str.encode("utf-8")) > MAX_JSON_SIZE_BYTES:
            return False

        # Encode the JSON string to base64
        encoded_bytes = base64.b64encode(json_str.encode("utf-8"))
        encoded_str = encoded_bytes.decode("ascii")

        # Store the result in the global list
        DATA_TO_TRANSFER.append(encoded_str)

        return True

    except Exception:
        # Any exception (e.g., serialization error, encoding error) results in a False return
        return False