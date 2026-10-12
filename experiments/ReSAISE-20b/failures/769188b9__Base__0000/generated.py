import urllib.request
from urllib.error import URLError, HTTPError
import hmac

# Global mapping of resource URLs to their expected cryptographic signatures.
# Example: {"https://example.com/doc1.pdf": "abcd1234efgh5678"}
DOC_HASHES = {
    # Add actual URL:signature pairs here
}

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the expected
    signature for a document hosted at `resource_url`.

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
        non-200 HTTP status, or URL not found in DOC_HASHES).
    """
    # Verify that the resource URL is known
    expected_sig = DOC_HASHES.get(resource_url)
    if expected_sig is None:
        raise IOError(f"Unknown resource URL: {resource_url}")

    # Attempt to access the document to ensure it is reachable
    try:
        with urllib.request.urlopen(resource_url, timeout=10) as resp:
            if resp.status != 200:
                raise IOError(f"Document not accessible, HTTP status {resp.status}")
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to access document at {resource_url}") from exc

    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(crypto_signature, expected_sig)