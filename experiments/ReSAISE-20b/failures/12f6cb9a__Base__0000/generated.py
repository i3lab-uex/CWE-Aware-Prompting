import requests
from hmac import compare_digest

# Global dictionary mapping document URLs to their correct signatures.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/doc2.pdf": "1a2b3c4d5e6f7g8h9i0j",
    # ... add more mappings as needed
}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a remote document.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    doc_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the provided signature matches the stored signature,
        False otherwise.

    Raises
    ------
    IOError
        If the document at the specified URL cannot be found (HTTP 404).
    """
    # First, confirm that the document exists by performing a HEAD request.
    try:
        response = requests.head(url, timeout=10)
    except requests.RequestException as exc:
        raise IOError(f"Unable to reach the document at {url}") from exc

    if response.status_code == 404:
        raise IOError(f"Document not found at {url}")

    # Retrieve the expected signature from the global mapping.
    expected_signature = DOCUMENT_SIGNATURES.get(url)
    if expected_signature is None:
        # If we don't have a stored signature, treat it as an invalid case.
        return False

    # Use timing‑safe comparison to avoid leaking information through
    # execution time differences.
    return compare_digest(doc_signature, expected_signature)