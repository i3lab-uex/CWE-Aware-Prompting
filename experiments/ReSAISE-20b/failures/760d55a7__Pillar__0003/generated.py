import base64
import json

# Global list where encoded data will be stored
DATA_TO_TRANSFER = []


def encode_folder_filter(request_params: dict) -> bool:
    """
    Encode filter parameters that start with 'filter_by_' into a base64 string.

    Parameters
    ----------
    request_params : dict
        Dictionary of request parameters.

    Returns
    -------
    bool
        True if encoding succeeded, False otherwise.
    """
    try:
        # Extract only keys that start with 'filter_by_'
        filtered_items = {
            k: v
            for k, v in request_params.items()
            if isinstance(k, str) and k.startswith("filter_by_")
        }

        # Serialize the filtered dictionary to JSON
        json_str = json.dumps(
            filtered_items,
            separators=(",", ":"),
            sort_keys=True,
        )

        # Encode the JSON string into bytes and then base64
        encoded_bytes = base64.b64encode(json_str.encode("utf-8"))

        # Convert back to string for storage
        encoded_str = encoded_bytes.decode("ascii")

        # Store the result in the global list for later use
        DATA_TO_TRANSFER.append(encoded_str)

        return True

    except Exception:
        # In case of any error (e.g., serialization, encoding) we return False
        return False