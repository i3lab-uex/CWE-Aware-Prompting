import requests
import hmac
from urllib.parse import urlparse

# Global dictionary mapping URLs to their expected signatures.
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "a3f5c8e2b1...",
    # "https://example.com/doc2.pdf": "d4c9e3f6a7...",
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the document at `doc_url` matches the provided cryptographic
    signature. The expected signature is looked up in the global
    DOCUMENT_SIGNATURES dictionary.

    Args:
        doc_url: The URL of the remote document.
        signature: The cryptographic signature supplied for the document.

    Returns:
        True if the signature matches the expected value, False otherwise.

    Raises:
        IOError: If the document cannot be accessed (e.g., network error,
                 non-200 status code, or invalid URL).
    """
    # Basic sanity check for the URL
    parsed = urlparse(doc_url)
    if not parsed.scheme or not parsed.netloc:
        raise IOError(f"Invalid URL: {doc_url}")

    try:
        # Use a reasonable timeout and verify SSL certificates
        response = requests.get(doc_url, timeout=10, allow_redirects=True)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise IOError(f"Failed to retrieve document from {doc_url}: {exc}") from exc

    # Retrieve the expected signature for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)
    if expected_sig is None:
        # If we have no record of the signature, treat as invalid
        return False

    # Compare signatures using constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(signature, expected_sig)