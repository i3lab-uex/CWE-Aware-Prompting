import json
import base64

# Global list where the encoded data will be stored
DATA_TO_TRANSFER = []

def encode_folder_filter(request_params: dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a secure base64 string.

    Parameters
    ----------
    request_params : dict
        Dictionary representing the request parameters. Only keys that start with
        'filter_by_' are considered for encoding.

    Returns
    -------
    bool
        True if the encoding succeeded and data was appended to DATA_TO_TRANSFER,
        False otherwise.

    Notes
    -----
    - The function serializes the filtered parameters as JSON before encoding.
    - `base64.urlsafe_b64encode` is used to avoid problematic characters in URLs.
    - No exceptions are raised; errors result in a False return value.
    """
    try:
        # Extract only relevant filter parameters
        filtered = {
            k: v for k, v in request_params.items()
            if isinstance(k, str) and k.startswith("filter_by_")
        }

        # If nothing to encode, still return True (nothing appended)
        if not filtered:
            return True

        # Serialize to JSON string
        json_str = json.dumps(filtered, separators=(",", ":"))

        # Encode as UTF-8 bytes and then to base64
        encoded_bytes = base64.urlsafe_b64encode(json_str.encode("utf-8"))

        # Store the resulting string in the global list
        DATA_TO_TRANSFER.append(encoded_bytes.decode("ascii"))
        return True

    except Exception:
        # Any unexpected error results in False; do not propagate exceptions
        return False