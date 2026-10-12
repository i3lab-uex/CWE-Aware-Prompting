import urllib.request
import urllib.error
from urllib.parse import urlparse, unquote
import hmac

# Global dictionary mapping document identifiers to their expected signatures.
DOC_SIGS = {
    # Example entries
    "example.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "report.docx": "1234567890abcdef",
}

def _get_doc_id(url: str) -> str:
    """
    Extract a document identifier from the URL.
    The identifier is assumed to be the last path component of the URL,
    percent‑decoded.  This simple strategy works for most common cases.
    """
    path = urlparse(url).path
    if not path:
        raise ValueError("URL does not contain a path component")
    doc_id = unquote(path.rsplit("/", 1)[-1])
    if not doc_id:
        raise ValueError("URL does not contain a document name")
    return doc_id

def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that the cryptographic signature supplied for a document
    matches the expected value stored in DOC_SIGS.

    Parameters:
        url (str): URL of the document to validate.
        sign_hash (str): Signature submitted with the document.

    Returns:
        bool: True if the signature matches the expected value,
              False otherwise.

    Raises:
        IOError: If the document at the provided URL is inaccessible.
    """
    # Ensure the document can be reached before checking its signature.
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            # We don't need the content; just verifying accessibility.
            if resp.status >= 400:
                raise IOError(f"Server returned status {resp.status}")
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        raise IOError(f"Unable to access document at {url}") from exc

    # Retrieve the expected signature for this document.
    doc_id = _get_doc_id(url)
    expected_sig = DOC_SIGS.get(doc_id)

    if expected_sig is None:
        # No known signature for this document.
        return False

    # Use constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(sign_hash, expected_sig)