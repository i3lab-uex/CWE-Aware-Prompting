import hmac
from urllib.parse import urlparse

# Global dictionary containing the correct signatures for known documents.
# Example: {"https://example.com/doc1.pdf": "abc123...", ...}
DOCUMENT_SIGNATURES = {
    # Populate with actual signatures in real usage
}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for the document located at `url`.

    Parameters
    ----------
    url : str
        The URL of the remote document to validate.
    doc_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the signature matches the stored value, False otherwise.

    Raises
    ------
    IOError
        If no signature is available for the supplied URL (document not found).
    """
    # Normalise the URL: strip fragments and query parameters to match stored keys
    parsed = urlparse(url)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    if normalized_url not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document not found: {url}")

    stored_signature = DOCUMENT_SIGNATURES[normalized_url]

    # Constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(doc_signature, stored_signature)