import base64
import json

# Global list to hold encoded data for further processing
DATA_TO_TRANSFER = []


def encode_folder_filter(request_params: dict) -> bool:
    """
    Encodes filter parameters from the request dictionary into a secure base64 string.
    Only keys that start with 'filter_by_' are considered.

    Parameters
    ----------
    request_params : dict
        Dictionary representing the request parameters.

    Returns
    -------
    bool
        True if encoding succeeded, False otherwise.
    """
    try:
        # Filter keys that start with 'filter_by_'
        filtered = {
            k: v for k, v in request_params.items() if isinstance(k, str) and k.startswith("filter_by_")
        }

        # If nothing to encode, consider it a success but do not add empty entry
        if not filtered:
            return True

        # Serialize to JSON string; use separators to reduce size
        json_str = json.dumps(filtered, separators=(",", ":"))

        # Encode the JSON string to bytes and then base64
        encoded_bytes = base64.b64encode(json_str.encode("utf-8"))

        # Store the result in the global list
        DATA_TO_TRANSFER.append(encoded_bytes.decode("ascii"))

        return True

    except Exception:
        # Any exception (e.g., memory error, type errors) results in False
        return False