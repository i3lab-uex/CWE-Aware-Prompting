import hashlib
import urllib.request
from urllib.error import HTTPError, URLError

# Global dictionary containing correct signatures for documents.
# Example: DOCUMENT_SIGNATURES = {"https://example.com/doc1.pdf": "abc123...", ...}
DOCUMENT_SIGNATURES: dict[str, str] = {}

def _is_url_accessible(url: str) -> bool:
    """
    Check if the given URL can be reached. Raises IOError if not.
    """
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            # HTTP 200-299 indicates success
            if not (200 <= response.getcode() < 300):
                raise IOError(f"URL returned non-success status: {response.getcode()}")
        return True
    except (HTTPError, URLError) as exc:
        raise IOError(f"Could not access URL '{url}': {exc}") from exc

def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a document identified by `doc_link`.

    Parameters
    ----------
    doc_link : str
        URL of the document to validate.
    check_signature : str
        Signature string provided for verification.

    Returns
    -------
    bool
        True if the signature matches, False otherwise.

    Raises
    ------
    IOError
        If the document URL cannot be reached.
    """
    # Ensure the document exists before checking signature
    _is_url_accessible(doc_link)

    # Retrieve stored signature; if missing, treat as mismatch
    stored_sig = DOCUMENT_SIGNATURES.get(doc_link)
    if stored_sig is None:
        return False

    # For security, compare using constant-time comparison
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _constant_time_compare(check_signature, stored_sig)