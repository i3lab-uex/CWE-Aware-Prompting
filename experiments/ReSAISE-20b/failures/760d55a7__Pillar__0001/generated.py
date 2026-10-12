import base64
import json
from typing import Dict, List

# Global list to store encoded data for further processing
DATA_TO_TRANSFER: List[str] = []


def encode_folder_filter(request_params: Dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a secure base64 string.
    Only keys that start with 'filter_by_' are considered.

    Args:
        request_params (dict): Dictionary representing the request parameters.

    Returns:
        bool: True if encoding succeeds, False otherwise.
    """
    try:
        # Filter relevant keys
        filtered = {k: v for k, v in request_params.items() if isinstance(k, str) and k.startswith("filter_by_")}

        # Serialize to JSON string
        json_str = json.dumps(filtered, separators=(",", ":"), ensure_ascii=False)

        # Encode to base64 bytes
        encoded_bytes = base64.urlsafe_b64encode(json_str.encode("utf-8"))

        # Store the encoded string in the global list
        DATA_TO_TRANSFER.append(encoded_bytes.decode("ascii"))

        return True
    except Exception:
        # Do not propagate exceptions; just indicate failure
        return False