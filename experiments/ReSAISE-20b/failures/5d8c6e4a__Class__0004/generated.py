import requests
import hmac

# Example pre‑defined signatures dictionary (populated elsewhere in the application)
DOCUMENT_SIGNATURES = {
    # "https://example.com/doc1.pdf": "sha256:abcd1234...",
    # ...
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remote document by checking its cryptographic signature.

    Parameters
    ----------
    location : str
        The URL of the document to be verified.
    sign : str
        The cryptographic signature claimed for the document.

    Returns
    -------
    bool
        True if the provided signature matches the expected one, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # 1. Retrieve the document to confirm it is reachable
    try:
        response = requests.get(location, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Unable to retrieve document at {location}") from exc

    # 2. Lookup the expected signature
    expected_sign = DOCUMENT_SIGNATURES.get(location)
    if expected_sign is None:
        # No signature stored for this URL; treat as invalid
        return False

    # 3. Compare signatures using a timing‑attack resistant comparison
    return hmac.compare_digest(sign, expected_sign)