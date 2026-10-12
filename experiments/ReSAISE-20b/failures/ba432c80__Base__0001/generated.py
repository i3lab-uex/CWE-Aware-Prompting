import hmac
import requests

# Example global dictionary mapping URLs to their expected signatures.
# In real usage this would be populated from a secure source.
DOC_SIGS = {
    "https://example.com/doc1.pdf": "a3f5c9e2b7d4...",
    # Add more URL:signature pairs as needed
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that a document at the given URL is accessible and that its
    cryptographic signature matches the expected value.

    Args:
        url: URL of the document to validate.
        sign_hash: Cryptographic signature submitted with the document.

    Returns:
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises:
        IOError: If the document at the provided URL is inaccessible.
    """
    # Ensure the URL is reachable
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        if response.status_code != 200:
            raise IOError(f"Document not accessible: HTTP {response.status_code}")
    except requests.RequestException as e:
        raise IOError(f"Could not access document at {url}: {e}") from e

    # Retrieve the expected signature for this URL
    expected_sig = DOC_SIGS.get(url)
    if expected_sig is None:
        # No known signature for this URL; treat as invalid
        return False

    # Use constant‑time comparison to mitigate timing attacks (CWE‑347)
    return hmac.compare_digest(sign_hash, expected_sig)