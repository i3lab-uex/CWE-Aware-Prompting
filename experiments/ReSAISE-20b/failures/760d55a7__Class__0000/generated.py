import base64
import json

# Global list used to store the encoded data for further processing.
DATA_TO_TRANSFER = []

def encode_folder_filter(request_params: dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a base64 string.

    Parameters
    ----------
    request_params : dict
        Dictionary representing the request parameters.

    Returns
    -------
    bool
        True if encoding succeeds, False otherwise.
    """
    # Safety: limit the number of keys to process to avoid excessive memory usage
    MAX_KEYS = 1000

    try:
        # Filter keys that start with 'filter_by_'
        filtered_items = {
            k: v
            for k, v in request_params.items()
            if isinstance(k, str) and k.startswith("filter_by_")
        }

        # Enforce a maximum number of keys to prevent uncontrolled resource consumption
        if len(filtered_items) > MAX_KEYS:
            # Too many keys; abort to protect resources
            return False

        # Serialize the filtered dictionary to JSON.
        json_bytes = json.dumps(filtered_items, separators=(",", ":")).encode("utf-8")

        # Base64 encode the JSON bytes.
        encoded_str = base64.urlsafe_b64encode(json_bytes).decode("ascii")

        # Store the encoded data in the global list for later use.
        DATA_TO_TRANSFER.append(encoded_str)

        return True
    except Exception:
        # Any exception (e.g., serialization error) results in a failure.
        return False