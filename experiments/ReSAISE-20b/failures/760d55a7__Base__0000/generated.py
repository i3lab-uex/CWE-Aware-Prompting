import json
import base64

# Global list where the encoded data will be stored.
DATA_TO_TRANSFER = []

def encode_folder_filter(request_params: dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a secure base64 string.
    
    Only keys that start with 'filter_by_' are considered. The resulting dictionary
    is serialized to JSON, then base64-encoded and appended to the global 
    DATA_TO_TRANSFER list.

    Parameters
    ----------
    request_params : dict
        Dictionary representing the request parameters.

    Returns
    -------
    bool
        True if encoding succeeded and data was stored, False otherwise.
    
    Notes
    -----
    - A size limit is imposed to mitigate CWE-770 (resource exhaustion).
      If the serialized JSON exceeds 1 MB, the function returns False.
    - The function does not raise any exceptions; all errors are handled
      internally and result in a False return value.
    """
    try:
        # Filter keys that start with 'filter_by_'
        filtered = {
            k: v for k, v in request_params.items()
            if isinstance(k, str) and k.startswith('filter_by_')
        }

        # Serialize to JSON
        json_str = json.dumps(filtered, separators=(',', ':'))

        # Enforce a reasonable size limit (1 MB)
        MAX_BYTES = 1_048_576
        if len(json_str.encode('utf-8')) > MAX_BYTES:
            return False

        # Base64 encode
        encoded_bytes = base64.b64encode(json_str.encode('utf-8'))
        encoded_str = encoded_bytes.decode('ascii')

        # Store the result
        DATA_TO_TRANSFER.append(encoded_str)
        return True

    except Exception:
        # Any unexpected error results in a False return value
        return False