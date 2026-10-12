import base64
import json

# Global list to store the encoded data for further processing
DATA_TO_TRANSFER = []

def encode_folder_filter(request_params: dict) -> bool:
    """
    Encode filter parameters from the request dictionary into a secure base64 string.
    Only keys that start with 'filter_by_' are considered.

    Parameters
    ----------
    request_params : dict
        Dictionary containing request parameters.

    Returns
    -------
    bool
        True if encoding succeeded, False otherwise.
    """
    try:
        # Extract only the relevant filter parameters
        filters = {k: v for k, v in request_params.items() if k.startswith("filter_by_")}

        # If no filters were found, nothing to encode
        if not filters:
            return False

        # Serialize the filter dictionary to a JSON string
        json_str = json.dumps(filters, separators=(",", ":"))

        # Optional: enforce a reasonable size limit to avoid CWE-770
        MAX_SIZE_BYTES = 10 * 1024  # 10 KiB limit
        if len(json_str.encode("utf-8")) > MAX_SIZE_BYTES:
            # Too large to encode safely
            return False

        # Encode the JSON string using base64 (URL-safe variant)
        encoded_bytes = base64.urlsafe_b64encode(json_str.encode("utf-8"))
        encoded_str = encoded_bytes.decode("ascii")

        # Store the encoded string in the global list
        DATA_TO_TRANSFER.append(encoded_str)

        return True

    except Exception:
        # Any exception (e.g., serialization error, encoding error) results in failure
        return False