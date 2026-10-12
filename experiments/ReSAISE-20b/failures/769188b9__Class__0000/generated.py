import requests
from hmac import compare_digest

# Global dictionary containing the expected cryptographic signatures for each document.
# Example: {"https://example.com/doc1.pdf": "abc123", ...}
DOC_HASHES = {
    # Populate with actual mappings in real use
}

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that the cryptographic signature supplied for a remote document matches
    the expected value stored in DOC_HASHES.

    Parameters
    ----------
    resource_url : str
        URL of the document to validate.
    crypto_signature : str
        Signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    IOError
        If the document at ``resource_url`` cannot be fetched (network error,
        non-200 status code, etc.).
    """
    # Ensure the URL is reachable before performing signature validation.
    try:
        response = requests.head(resource_url, timeout=5)
        if response.status_code != 200:
            raise IOError(f"Document not accessible: HTTP {response.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Unable to access document at {resource_url}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOC_HASHES.get(resource_url)
    if expected_sig is None:
        # No known signature for this URL; treat as invalid.
        return False

    # Use constant‑time comparison to avoid timing attacks.
    return compare_digest(crypto_signature, expected_sig)