import requests
from urllib.parse import urlparse
import hmac

# Global mapping of document URLs to their expected cryptographic signatures.
DOC_HASHES = {
    # Example entries (URL: expected signature)
    "https://example.com/docs/report.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/docs/terms.txt":  "1234567890abcdef",
}

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    value for a document located at ``resource_url``.
    
    Parameters
    ----------
    resource_url : str
        The URL of the document to validate.
    crypto_signature : str
        The cryptographic signature submitted with the document.
    
    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.
    
    Raises
    ------
    IOError
        If the document at ``resource_url`` is inaccessible (e.g., network error,
        4xx/5xx status code, or malformed URL).
    """
    # Basic input validation
    if not isinstance(resource_url, str) or not isinstance(crypto_signature, str):
        raise ValueError("Both resource_url and crypto_signature must be strings")

    # Ensure the URL is well‑formed
    parsed = urlparse(resource_url)
    if not parsed.scheme or not parsed.netloc:
        raise IOError(f"Malformed URL: {resource_url}")

    try:
        # Use a HEAD request to confirm the resource exists without downloading it.
        response = requests.head(resource_url, timeout=5)
        if not response.ok:
            raise IOError(f"Document inaccessible (status {response.status_code}): {resource_url}")
    except requests.RequestException as exc:
        raise IOError(f"Could not access document at {resource_url}") from exc

    # Retrieve the expected signature for this URL
    expected_sig = DOC_HASHES.get(resource_url)
    if expected_sig is None:
        # If we have no record of this document, treat it as unauthenticated
        return False

    # Perform a constant‑time comparison to mitigate timing attacks (CWE‑693)
    return hmac.compare_digest(expected_sig, crypto_signature)