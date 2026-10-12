import requests
from urllib.parse import urlparse

# Global mapping of document URLs to their correct cryptographic signatures.
# In a real system this would be stored securely and not hard‑coded.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "abc123def456",
    "https://example.com/doc2.txt": "789ghi012jkl",
    # ... add more entries as needed ...
}

def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the one stored
    for the document at `doc_link`.

    Parameters
    ----------
    doc_link : str
        The URL of the document to validate.
    check_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the signature matches, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved or the URL is not recognized.
    """
    # Ensure that the link is a well‑formed HTTP/HTTPS URL
    parsed = urlparse(doc_link)
    if parsed.scheme not in ("http", "https"):
        raise IOError(f"Unsupported URL scheme: {parsed.scheme}")

    # Attempt to fetch the document to confirm it exists.
    try:
        response = requests.head(doc_link, allow_redirects=True, timeout=5)
        if response.status_code != 200:
            raise IOError(f"Document not found (HTTP {response.status_code})")
    except requests.RequestException as e:
        raise IOError(f"Unable to access document: {e}")

    # Retrieve the expected signature from the global mapping
    expected_signature = DOCUMENT_SIGNATURES.get(doc_link)
    if expected_signature is None:
        raise IOError("Document signature unknown for the provided URL")

    # Constant‑time comparison to mitigate timing attacks
    return _constant_time_compare(expected_signature, check_signature)

def _constant_time_compare(a: str, b: str) -> bool:
    """
    Compare two strings in constant time to avoid timing side‑channels.
    """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode(), b.encode()):
        result |= x ^ y
    return result == 0