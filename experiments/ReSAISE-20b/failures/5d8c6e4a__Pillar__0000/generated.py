import requests
import hmac

# Predefined dictionary of known valid signatures for remote documents.
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "5f2d3e...",
    # "https://example.com/doc2.txt": "a1b2c3..."
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remote document by verifying its cryptographic signature.

    Parameters
    ----------
    location : str
        The URL of the document to be verified.
    sign : str
        The cryptographic signature provided for validation.

    Returns
    -------
    bool
        True if the signature matches the stored value; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # 1. Ensure the document is reachable
    try:
        response = requests.get(location, timeout=10)
        response.raise_for_status()
    except Exception as exc:
        raise IOError(f"Unable to retrieve document from {location}") from exc

    # 2. Retrieve the expected signature
    expected_sig = DOCUMENT_SIGNATURES.get(location)
    if expected_sig is None:
        # If the document is unknown, treat it as unauthenticated
        return False

    # 3. Compare signatures using a constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_sig, sign)