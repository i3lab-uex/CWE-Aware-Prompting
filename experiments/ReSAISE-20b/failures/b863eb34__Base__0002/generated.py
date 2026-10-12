import requests
import hmac

# Global dictionary mapping document URLs to their correct signatures.
DOCUMENT_SIGNATURES = {
    # Example entries:
    "https://example.com/doc1.pdf": "a3f5c2b4d6e7...",
    "https://example.com/doc2.pdf": "9f8e7d6c5b4a...",
    # Add more URL → signature mappings here.
}


def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the cryptographic signature provided for a remote document
    matches the expected signature stored in DOCUMENT_SIGNATURES.

    Parameters
    ----------
    doc_url : str
        The URL of the document to verify.
    signature : str
        The cryptographic signature provided for the document.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed at the given URL (e.g., network error,
        HTTP status >= 400, or timeout).
    """
    # Validate that we have a known signature for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)
    if expected_sig is None:
        # Unknown document URL – treat as invalid.
        return False

    try:
        # Attempt to fetch the document; we only care about accessibility,
        # not the content itself.
        resp = requests.get(doc_url, timeout=10)
        resp.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Any problem accessing the URL should raise an IOError.
        raise IOError(f"Unable to access document at {doc_url}") from exc

    # Use a constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(signature, expected_sig)