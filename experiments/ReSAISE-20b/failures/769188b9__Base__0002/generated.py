import requests
import hmac

# Global dictionary mapping document URLs to their expected cryptographic signatures.
DOC_HASHES = {
    # Example entries; replace with actual values in production
    "https://example.com/doc1.pdf": "a3f5c8e2b7d9...",
    "https://example.com/doc2.pdf": "4f1e6b3d8a0c...",
    # ...
}

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    value for a document located at `resource_url`.

    Parameters
    ----------
    resource_url : str
        URL of the document to validate.
    crypto_signature : str
        Cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    IOError
        If the document at `resource_url` cannot be accessed (e.g., network error,
        4xx/5xx HTTP status).
    """
    # First, ensure the document is reachable.
    try:
        response = requests.head(resource_url, timeout=5)
        if not response.ok:
            raise IOError(f"Document inaccessible: HTTP {response.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Failed to access document at {resource_url}") from exc

    # Retrieve the expected signature.
    expected_sig = DOC_HASHES.get(resource_url)
    if expected_sig is None:
        # Unknown document; treat as authentication failure.
        return False

    # Use constant‑time comparison to mitigate timing attacks (CWE-347).
    return hmac.compare_digest(expected_sig, crypto_signature)