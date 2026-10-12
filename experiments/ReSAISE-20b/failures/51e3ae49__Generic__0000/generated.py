import requests
import hmac

# Example global dictionary of valid signatures for documents.
# In a real system this would be populated from a secure source.
DOCUMENT_SIGNATURES = {
    # "https://example.com/doc1.pdf": "abc123...",
    # "https://example.com/doc2.txt": "def456...",
}

def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a document at `file_url`.

    Parameters
    ----------
    file_url : str
        URL of the document to validate.
    crypt_signature : str
        Cryptographic signature provided for verification.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be found (HTTP 404 or connection error).
    """
    # Check that the URL is reachable
    try:
        response = requests.head(file_url, allow_redirects=True, timeout=10)
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Unable to reach {file_url}") from exc

    if response.status_code == 404:
        raise IOError(f"Document not found: {file_url}")
    if response.status_code >= 400:
        raise IOError(f"Error accessing document: {file_url} (status {response.status_code})")

    # Retrieve the stored signature for this URL
    expected_signature = DOCUMENT_SIGNATURES.get(file_url)
    if expected_signature is None:
        # If we don't have a stored signature, treat it as invalid
        return False

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(crypt_signature, expected_signature)