import requests
import hmac

# Pre‑defined mapping of document URLs to their authentic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries (URL : signature)
    "https://example.com/doc1.pdf": "a3f9c8b7e2d4...",
    # Add more entries as needed.
}

def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validates the integrity of a remote document by checking its cryptographic signature.

    Parameters
    ----------
    url : str
        The URL of the document to be verified.
    crypt_signature : str
        The signature supplied for verification.

    Returns
    -------
    bool
        True if the supplied signature matches the authentic one; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Attempt to fetch the document to ensure it is reachable.
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Could not retrieve document from {url}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOCUMENT_SIGNATURES.get(url)
    if expected_sig is None:
        # If the URL isn't known, we cannot validate; treat as failure.
        return False

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sig, crypt_signature)