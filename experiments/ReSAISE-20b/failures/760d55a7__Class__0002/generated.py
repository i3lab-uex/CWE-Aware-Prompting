import json
import base64

# Global list to hold the encoded data for further processing
DATA_TO_TRANSFER = []

def encode_folder_filter(request_params: dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a secure base64 string.

    Parameters
    ----------
    request_params : dict
        Dictionary representing the request parameters. Only keys that start with
        'filter_by_' are considered.

    Returns
    -------
    bool
        True if the encoding was successful and data was appended to
        DATA_TO_TRANSFER, False otherwise.
    """
    try:
        # Extract only relevant keys
        filter_params = {
            k: v for k, v in request_params.items() if k.startswith("filter_by_")
        }

        # If no filter parameters, nothing to encode
        if not filter_params:
            return False

        # Serialize to JSON string
        json_str = json.dumps(filter_params, separators=(",", ":"))

        # Limit size to avoid uncontrolled resource consumption
        MAX_BYTES = 10 * 1024  # 10 KB
        json_bytes = json_str.encode("utf-8")
        if len(json_bytes) > MAX_BYTES:
            # Too large to encode safely
            return False

        # Encode with base64
        encoded_bytes = base64.urlsafe_b64encode(json_bytes)
        encoded_str = encoded_bytes.decode("ascii")

        # Store the result
        DATA_TO_TRANSFER.append(encoded_str)
        return True

    except Exception:
        # No exception should propagate; failure returns False
        return False