import requests
import hmac

# Global dictionary mapping document URLs to their correct cryptographic signatures.
# In a real application this would be populated from a secure source.
DOCUMENT_SIGNATURES = {
    # Example: "https://example.com/doc1.pdf": "abcdef123456...",
}

def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the stored
    signature for a document located at ``doc_link`` and that the
    document is accessible.

    Parameters
    ----------
    doc_link : str
        URL of the remote document to validate.
    check_signature : str
        Cryptographic signature provided for verification.

    Returns
    -------
    bool
        ``True`` if the supplied signature matches the stored one and
        the document is accessible; otherwise ``False``.

    Raises
    ------
    IOError
        If the document cannot be found (HTTP 404) or is otherwise
        unreachable.
    """
    # First, confirm the document exists and is reachable.
    try:
        head_resp = requests.head(doc_link, allow_redirects=True, timeout=10)
    except requests.RequestException as exc:
        raise IOError(f"Unable to reach the document at {doc_link}: {exc}") from exc

    if head_resp.status_code == 404:
        raise IOError(f"Document not found at {doc_link} (404).")

    if head_resp.status_code >= 400:
        raise IOError(f"Error accessing document at {doc_link}: HTTP {head_resp.status_code}")

    # Retrieve the stored signature for this document.
    expected_sig = DOCUMENT_SIGNATURES.get(doc_link)
    if expected_sig is None:
        # If the document link isn't known, treat it as a mismatch.
        return False

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(check_signature, expected_sig)