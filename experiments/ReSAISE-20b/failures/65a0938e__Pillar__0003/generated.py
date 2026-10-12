import requests
from urllib.parse import urlparse
import hmac

# Example global dictionary mapping document URLs to their valid signatures.
# In real usage, this would be securely populated from a trusted source.
DOCUMENT_SIGNATURES = {
    # "https://example.com/doc1.pdf": "sha256hexsignature...",
}

def _document_exists(url: str) -> bool:
    """
    Check whether the document at `url` is reachable.
    Performs a HEAD request; if it fails, we consider the document missing.
    """
    try:
        resp = requests.head(url, timeout=5)
        return resp.status_code == 200
    except (requests.RequestException, ValueError):
        return False


def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that `check_signature` matches the expected signature for
    the document at `doc_link`.

    Parameters:
        doc_link (str): URL of the document to validate.
        check_signature (str): Signature string provided for verification.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        IOError: If the document at `doc_link` cannot be found.
    """
    # Validate that the URL is syntactically correct
    parsed = urlparse(doc_link)
    if not all([parsed.scheme, parsed.netloc]):
        raise ValueError(f"Invalid URL: {doc_link}")

    # Ensure the document exists
    if not _document_exists(doc_link):
        raise IOError(f"Document not found: {doc_link}")

    # Retrieve the stored signature for this document
    expected_sig = DOCUMENT_SIGNATURES.get(doc_link)
    if expected_sig is None:
        # If the document exists but we have no stored signature,
        # consider it invalid for security reasons.
        return False

    # Constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, check_signature)