import requests
from urllib.parse import urlparse

# Global mapping of document URLs to their expected signatures.
DOCUMENT_SIGNATURES = {
    # Example entries; replace with real data in production
    "https://example.com/doc1.pdf": "abc123def456",
    "https://example.com/doc2.pdf": "789xyz012uvw",
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the document at *doc_url* is reachable and that its
    cryptographic signature matches the expected value stored in
    DOCUMENT_SIGNATURES.

    Parameters
    ----------
    doc_url : str
        The URL of the document to verify.
    signature : str
        The cryptographic signature provided for the document.

    Returns
    -------
    bool
        True if the URL is reachable and the signature matches, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed (e.g., network error, 404, etc.).
    """
    # Ensure the URL uses HTTPS to mitigate MITM attacks
    parsed = urlparse(doc_url)
    if parsed.scheme.lower() != "https":
        raise ValueError("Non‑HTTPS URLs are not allowed for document verification")

    try:
        # Use a HEAD request to check reachability without downloading the whole file.
        response = requests.head(doc_url, allow_redirects=True, timeout=10)
        if response.status_code >= 400:
            raise IOError(f"Document at {doc_url} returned status code {response.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Unable to access document at {doc_url}: {exc}") from exc

    # Retrieve the expected signature for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)

    # If the document is not registered, treat it as invalid
    if expected_sig is None:
        return False

    # Perform a constant‑time comparison to mitigate timing attacks
    if _constant_time_compare(expected_sig, signature):
        return True

    return False


def _constant_time_compare(a: str, b: str) -> bool:
    """
    Compare two strings in constant time to avoid leaking timing information.
    """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode(), b.encode()):
        result |= x ^ y
    return result == 0