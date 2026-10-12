import requests
from urllib.parse import urlparse

# Global dictionary mapping URLs to their expected cryptographic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries; replace with actual URLs and signatures.
    "https://example.com/doc1.pdf": "abc123def456",
    "https://example.org/report.txt": "789ghi012jkl",
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the cryptographic signature of a remote document matches
    the expected value stored in DOCUMENT_SIGNATURES.

    Parameters:
        doc_url (str): URL of the document to be verified.
        signature (str): Signature provided for the document.

    Returns:
        bool: True if the signature matches the expected value, False otherwise.

    Raises:
        IOError: If the document cannot be accessed (network error, HTTP error,
                 or invalid URL).
    """
    # Basic validation of the URL.
    parsed = urlparse(doc_url)
    if not parsed.scheme or not parsed.netloc:
        raise IOError(f"Invalid URL: {doc_url}")

    try:
        # Perform a HEAD request to check availability without downloading the whole file.
        response = requests.head(doc_url, timeout=10, allow_redirects=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Convert any network/HTTP error into an IOError to satisfy the spec.
        raise IOError(f"Failed to access document at {doc_url}: {exc}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)
    if expected_sig is None:
        # If the URL is unknown, we cannot verify it; treat as invalid.
        return False

    # Compare signatures in a constant‑time manner to avoid timing attacks.
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _constant_time_compare(signature, expected_sig)