import requests
from hmac import compare_digest

# Global mapping of document URLs to their correct cryptographic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries (URL: signature)
    "https://example.com/docs/contract.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/docs/report.txt":  "1234567890abcdef",
    # Add real entries as needed
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the cryptographic signature of a remote document matches
    the expected value stored in DOCUMENT_SIGNATURES.

    Parameters
    ----------
    doc_url : str
        URL of the document to verify.
    signature : str
        Cryptographic signature provided for the document.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed (network error, 404, etc.).
    """
    # First ensure we can reach the document.
    try:
        response = requests.get(doc_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        # Wrap any request-related exception in an IOError.
        raise IOError(f"Unable to access document at {doc_url}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)

    # If we don't have a stored signature for this URL, treat it as invalid.
    if expected_sig is None:
        return False

    # Perform a constant‑time comparison to mitigate timing attacks.
    return compare_digest(signature, expected_sig)