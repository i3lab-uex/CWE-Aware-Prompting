import requests
import hmac

# Global mapping of document URLs to their correct cryptographic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries; replace with actual data
    "https://example.com/doc1.pdf": "a3f5c2b9e7d8...",
    "https://example.com/doc2.pdf": "f1e4b9c3d6a0...",
    # ...
}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that a document at `url` is reachable and that its cryptographic
    signature matches the expected one stored in DOCUMENT_SIGNATURES.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    doc_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the provided signature matches the stored signature for
        this document, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved (e.g., HTTP 404 or network error).
    """
    # Ensure the document exists by performing a lightweight HEAD request.
    try:
        head_resp = requests.head(url, allow_redirects=True, timeout=10)
        if head_resp.status_code == 404:
            raise IOError(f"Document not found at URL: {url}")
        # For other non-success status codes, raise an exception.
        head_resp.raise_for_status()
    except requests.RequestException as e:
        # Convert any request-related errors into IOError for consistency.
        raise IOError(f"Unable to access document at {url}: {e}") from e

    # Retrieve the expected signature for this URL.
    expected_sig = DOCUMENT_SIGNATURES.get(url)
    if expected_sig is None:
        # No signature known for this document; treat as invalid.
        return False

    # Perform a constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(doc_signature, expected_sig)