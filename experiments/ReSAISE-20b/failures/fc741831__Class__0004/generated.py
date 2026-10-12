import requests
import hmac

# Pre‑defined mapping of document URLs to their authentic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries (URL: signature)
    "https://example.com/doc1.pdf": "a3f5c7e9b8d2...",
    # Add real entries here.
}

def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate that the document at `url` is reachable and its signature matches
    the expected value stored in DOCUMENT_SIGNATURES.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    crypt_signature : str
        The cryptographic signature supplied for validation.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the provided URL.
    """
    # Ensure the document can be fetched
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Unable to retrieve document from {url}") from exc

    # Retrieve the expected signature for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(url)
    if expected_sig is None:
        # If no signature exists for this URL, consider it invalid
        return False

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(crypt_signature, expected_sig)