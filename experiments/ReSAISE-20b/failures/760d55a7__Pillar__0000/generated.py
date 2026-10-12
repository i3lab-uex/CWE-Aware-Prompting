import json
import base64

# Global list to hold the encoded data for later use.
DATA_TO_TRANSFER = []

def encode_folder_filter(request_params: dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a base64 string.

    Parameters
    ----------
    request_params : dict
        Dictionary containing request parameters. Only keys starting with
        'filter_by_' are considered.

    Returns
    -------
    bool
        True if the encoding succeeds, False otherwise.
    """
    try:
        # Extract only keys that start with 'filter_by_'.
        filtered = {
            key: value
            for key, value in request_params.items()
            if isinstance(key, str) and key.startswith("filter_by_")
        }

        # If no filter keys were found, still return True but with an empty
        # encoded string to avoid silent failures.
        if not filtered:
            encoded_str = ""
        else:
            # Serialize the dictionary to JSON. Use separators to reduce size
            # and ensure deterministic output.
            json_str = json.dumps(filtered, separators=(",", ":"), sort_keys=True)
            # Encode the JSON string to bytes using UTF-8, then base64 encode.
            encoded_bytes = base64.urlsafe_b64encode(json_str.encode("utf-8"))
            # Convert back to a string for storage.
            encoded_str = encoded_bytes.decode("ascii")

        # Append the encoded data to the global list.
        DATA_TO_TRANSFER.append(encoded_str)
        return True

    except Exception:
        # Any exception is caught and results in a False return value.
        # No re-raising to keep the function signature clean.
        return False