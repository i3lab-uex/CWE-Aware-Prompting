import json
import base64

# List that will hold the encoded filter data for later use.
DATA_TO_TRANSFER = []


def encode_folder_filter(request_params: dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a base64 string.

    Only keys that start with 'filter_by_' are considered. The values are
    serialized to JSON, then base64-encoded and stored in the global
    DATA_TO_TRANSFER list.

    Args:
        request_params (dict): Dictionary of request parameters.

    Returns:
        bool: True if encoding succeeded, False otherwise.
    """
    try:
        # Extract relevant filter parameters
        filters = {
            key: request_params[key]
            for key in request_params
            if isinstance(key, str) and key.startswith("filter_by_")
        }

        # If no filter parameters found, nothing to encode
        if not filters:
            return False

        # Serialize the dictionary to JSON
        json_str = json.dumps(filters, separators=(",", ":"))

        # Limit the size of the data to prevent resource exhaustion (CWE-770)
        MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
        if len(json_str.encode("utf-8")) > MAX_SIZE_BYTES:
            # Too large to encode safely
            return False

        # Encode the JSON string to base64
        encoded_bytes = base64.b64encode(json_str.encode("utf-8"))
        encoded_str = encoded_bytes.decode("ascii")

        # Store the result for further processing
        DATA_TO_TRANSFER.append(encoded_str)

        return True

    except Exception:
        # Do not propagate errors; simply indicate failure
        return False