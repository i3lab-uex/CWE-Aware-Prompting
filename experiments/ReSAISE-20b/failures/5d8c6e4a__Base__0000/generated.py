import requests
import hmac

# Pre‑defined dictionary of valid signatures for remote documents.
# Example: {"https://example.com/doc.pdf": "abcdef123456..."}
DOCUMENT_SIGNATURES = {
    # Populate with real URLs and their expected cryptographic signatures
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remote document by checking its cryptographic signature.

    Parameters
    ----------
    location : str
        The URL of the document to verify.
    sign : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the provided signature matches the expected one for the URL.
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Ensure we can fetch the file; raise IOError on failure
    try:
        response = requests.get(location, timeout=10)
        if not response.ok:
            raise IOError(f"Failed to retrieve document: {location} (status code {response.status_code})")
    except requests.RequestException as exc:
        raise IOError(f"Unable to retrieve document from {location}") from exc

    # Retrieve the expected signature for this URL
    expected_sign = DOCUMENT_SIGNATURES.get(location)
    if expected_sign is None:
        # If the URL is unknown, treat as invalid signature
        return False

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected_sign)