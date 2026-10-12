import json
import base64

# Global list to store encoded data for further processing
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
        True if encoding was successful, False otherwise.
    """
    try:
        # Extract only relevant filter keys
        filtered = {
            k: v for k, v in request_params.items() if isinstance(k, str) and k.startswith("filter_by_")
        }

        # If nothing to encode, return False
        if not filtered:
            return False

        # Serialize to JSON string; ensure ASCII for base64 encoding
        json_str = json.dumps(filtered, separators=(",", ":"), sort_keys=True)

        # Encode JSON string to bytes then base64
        encoded_bytes = base64.urlsafe_b64encode(json_str.encode("utf-8"))

        # Store the resulting string in the global list
        DATA_TO_TRANSFER.append(encoded_bytes.decode("ascii"))

        return True

    except Exception:
        # In case of any error, do not raise; simply indicate failure
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    sample_request = {
        "filter_by_status": "active",
        "filter_by_type": "folder",
        "page": 2,
        "limit": 50
    }
    success = encode_folder_filter(sample_request)
    print("Success:", success)
    print("DATA_TO_TRANSFER:", DATA_TO_TRANSFER)