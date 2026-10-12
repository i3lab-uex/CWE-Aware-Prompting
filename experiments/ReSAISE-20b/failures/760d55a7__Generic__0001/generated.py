import base64
import json

# List used to store the encoded data for further processing
DATA_TO_TRANSFER = []

def encode_folder_filter(request_params: dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a secure base64 string.
    
    Parameters
    ----------
    request_params : dict
        Dictionary containing request parameters. Only keys that start with
        'filter_by_' will be encoded.
    
    Returns
    -------
    bool
        True if the encoding succeeded, False otherwise.
    """
    try:
        # Extract only filter-related parameters
        filtered = {
            key: value
            for key, value in request_params.items()
            if isinstance(key, str) and key.startswith("filter_by_")
        }

        # If there are no filter parameters, nothing to encode
        if not filtered:
            return False

        # Serialize the dictionary to a JSON string with compact separators
        json_str = json.dumps(
            filtered,
            ensure_ascii=False,
            separators=(",", ":"),
        )

        # Encode the JSON string to bytes and then base64 encode
        encoded_bytes = base64.b64encode(json_str.encode("utf-8"))

        # Store the resulting string (decoded to str for readability)
        DATA_TO_TRANSFER.append(encoded_bytes.decode("ascii"))

        return True
    except Exception:
        # Any error (e.g., serialization, encoding) results in False
        return False