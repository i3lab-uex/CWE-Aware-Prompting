import json
import base64

# Global list to store encoded data for further processing.
DATA_TO_TRANSFER = []

def encode_folder_filter(request_params: dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a secure base64 string.
    
    Only keys that start with 'filter_by_' are considered. The resulting dictionary
    is JSON serialized and then base64 encoded. The encoded string is appended to
    the global DATA_TO_TRANSFER list.

    Parameters:
        request_params (dict): Dictionary representing request parameters.

    Returns:
        bool: True if encoding succeeded, False otherwise.
    """
    try:
        # Filter keys that start with 'filter_by_' and build a new dict.
        filtered = {k: v for k, v in request_params.items() if isinstance(k, str) and k.startswith("filter_by_")}

        # If no relevant keys are found, return False (nothing to encode).
        if not filtered:
            return False

        # Serialize the dictionary to a JSON string.
        # Use separators to minimize size and ensure deterministic output.
        json_str = json.dumps(filtered, separators=(",", ":"), sort_keys=True)

        # Limit the size of the JSON string to avoid uncontrolled resource consumption.
        MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
        if len(json_str.encode("utf-8")) > MAX_SIZE_BYTES:
            # Too large to encode safely.
            return False

        # Base64-encode the UTF-8 bytes of the JSON string.
        encoded_bytes = base64.b64encode(json_str.encode("utf-8"))

        # Convert bytes to string for storage.
        encoded_str = encoded_bytes.decode("ascii")

        # Append the encoded string to the global list.
        DATA_TO_TRANSFER.append(encoded_str)

        return True
    except Exception:
        # Swallow all exceptions to satisfy the "Raise: None" requirement.
        return False