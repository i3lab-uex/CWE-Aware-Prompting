import base64
import json

# Global list to store encoded data for further processing.
DATA_TO_TRANSFER = []

def encode_folder_filter(request_params: dict) -> bool:
    """
    Encode filter parameters from a request dictionary into a secure base64 string.

    Parameters
    ----------
    request_params : dict
        Dictionary representing the request parameters. Only keys that start with
        'filter_by_' will be considered.

    Returns
    -------
    bool
        True if encoding succeeded, False otherwise.
    """
    try:
        # Extract only the relevant filter parameters
        filters = {k: v for k, v in request_params.items() if k.startswith("filter_by_")}

        # Serialize to JSON string
        json_str = json.dumps(filters, separators=(",", ":"), ensure_ascii=False)

        # Encode the JSON string to bytes and then to base64
        encoded_bytes = base64.urlsafe_b64encode(json_str.encode("utf-8"))

        # Store the encoded string (decode to str for readability)
        DATA_TO_TRANSFER.append(encoded_bytes.decode("ascii"))

        return True
    except Exception:
        # No exceptions should propagate; just indicate failure.
        return False