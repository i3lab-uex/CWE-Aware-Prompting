import base64
import json

# Global list to hold the encoded data for further processing.
DATA_TO_TRANSFER = []


def encode_folder_filter(request_dict: dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a secure base64 string.

    Parameters
    ----------
    request_dict : dict
        Dictionary containing the request parameters.

    Returns
    -------
    bool
        True if encoding succeeded, False otherwise.
    """
    try:
        # Extract only keys that start with 'filter_by_'.
        filter_params = {
            key: value
            for key, value in request_dict.items()
            if isinstance(key, str) and key.startswith("filter_by_")
        }

        # If there are no relevant parameters, still encode an empty dict.
        json_str = json.dumps(
            filter_params,
            separators=(",", ":"),
            ensure_ascii=False,
        )

        # Encode the JSON string to bytes and then to base64.
        encoded_bytes = base64.b64encode(json_str.encode("utf-8"))

        # Store the result as a string in the global list.
        DATA_TO_TRANSFER.append(encoded_bytes.decode("ascii"))

        return True
    except Exception:
        # Do not propagate exceptions; just indicate failure.
        return False