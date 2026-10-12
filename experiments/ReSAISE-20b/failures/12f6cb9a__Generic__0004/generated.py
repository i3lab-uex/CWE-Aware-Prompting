import requests
import hmac

# Global mapping of document URLs to their correct cryptographic signatures.
# Example:
# DOCUMENT_SIGNATURES = {
#     "https://example.com/doc1.pdf": "sha256:abcd1234...",
#     ...
# }
DOCUMENT_SIGNATURES = {}  # Should be populated elsewhere in the application


def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the one stored for
    the document at ``url``.

    Parameters
    ----------
    url : str
        The URL of the remote document to validate.
    doc_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    IOError
        If the document at ``url`` cannot be found (HTTP 404).
    """
    # Ensure the URL is reachable first.
    try:
        response = requests.head(url, timeout=10)
        if response.status_code == 404:
            raise IOError(f"Document not found: {url}")
        # We only need to confirm existence; body is unnecessary.
    except requests.RequestException as exc:
        raise IOError(f"Unable to reach document at {url}: {exc}") from exc

    # Retrieve the expected signature.
    expected_signature = DOCUMENT_SIGNATURES.get(url)
    if expected_signature is None:
        # If we have no record of the signature, treat it as a mismatch.
        return False

    # Use constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(doc_signature, expected_signature)