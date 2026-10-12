import json
import base64

# Global list to store encoded data for further processing
DATA_TO_TRANSFER = []

# Maximum allowed size of the base64 encoded string (bytes). 10 KiB is a reasonable
# limit for typical filter parameters; adjust as needed.
MAX_ENCODED_SIZE = 10 * 1024


def encode_folder_filter(request_dict: dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a secure base64 string.

    Only keys starting with 'filter_by_' are considered. The resulting JSON is
    serialized, base64 encoded and appended to the global DATA_TO_TRANSFER list.

    Args:
        request_dict (dict): Dictionary representing the request parameters.

    Returns:
        bool: True if encoding was successful and size limits were respected,
              False otherwise.
    """
    try:
        # Extract relevant filter parameters
        filters = {
            key: value
            for key, value in request_dict.items()
            if isinstance(key, str) and key.startswith("filter_by_")
        }

        # If no filter parameters were found, nothing to encode
        if not filters:
            return False

        # Serialize the dictionary to a JSON string
        json_str = json.dumps(filters, separators=(",", ":"))

        # Encode the JSON string to bytes using UTF-8
        json_bytes = json_str.encode("utf-8")

        # Base64 encode the bytes
        encoded_bytes = base64.b64encode(json_bytes)

        # Enforce a size limit to mitigate CWE-770
        if len(encoded_bytes) > MAX_ENCODED_SIZE:
            return False

        # Store the encoded string (decode back to str for readability)
        DATA_TO_TRANSFER.append(encoded_bytes.decode("ascii"))

        return True

    except Exception:
        # Any exception (e.g., serialization errors, encoding problems) results in failure
        return False