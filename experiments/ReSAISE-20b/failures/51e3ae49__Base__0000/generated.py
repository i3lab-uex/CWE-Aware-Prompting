import requests
import hmac

# Global dictionary mapping document URLs to their correct cryptographic signatures.
# Example:
# DOCUMENT_SIGNATURES = {
#     "https://example.com/doc1.pdf": "abcd1234efgh5678",
#     ...
# }
DOCUMENT_SIGNATURES = {}  # placeholder – populate with actual signatures


def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a document located at `file_url`.

    Parameters
    ----------
    file_url : str
        The URL of the remote document to validate.
    crypt_signature : str
        The signature supplied for verification.

    Returns
    -------
    bool
        True if the provided signature matches the stored one, False otherwise.

    Raises
    ------
    IOError
        If the document at `file_url` cannot be found (HTTP 404 or similar).
    """
    # Check that the document exists; we only need a HEAD request to avoid downloading
    try:
        response = requests.head(file_url, allow_redirects=True, timeout=10)
    except requests.RequestException as exc:
        raise IOError(f"Unable to reach {file_url}") from exc

    if response.status_code == 404:
        raise IOError(f"Document not found: {file_url}")

    # Retrieve the expected signature from the global mapping
    expected_signature = DOCUMENT_SIGNATURES.get(file_url)
    if expected_signature is None:
        # If we don't have a signature for this URL, consider it invalid
        return False

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(crypt_signature, expected_signature)