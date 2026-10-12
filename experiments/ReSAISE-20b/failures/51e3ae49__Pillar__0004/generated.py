import urllib.request
from urllib.error import HTTPError, URLError
import hmac

# Example global mapping of document URLs to their correct signatures.
# In a real system this would be securely stored and accessed.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/doc2.pdf": "0123456789abcdef1234",
}

def _fetch_document(url: str) -> bytes:
    """
    Attempts to fetch the document from the given URL.
    Raises IOError if the resource cannot be retrieved.
    """
    try:
        with urllib.request.urlopen(url) as response:
            # Ensure we get a 2xx status code
            if not (200 <= response.status < 300):
                raise IOError(f"Unexpected status code {response.status} for URL: {url}")
            return response.read()
    except (HTTPError, URLError) as exc:
        raise IOError(f"Unable to retrieve document at {url}") from exc

def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Validates that the provided cryptographic signature matches the
    expected signature for the document located at `file_url`.

    Parameters:
        file_url (str): The URL of the remote document.
        crypt_signature (str): The signature to validate.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved.
    """
    # Ensure we can reach the URL (basic existence check)
    _fetch_document(file_url)

    expected_sig = DOCUMENT_SIGNATURES.get(file_url)
    if expected_sig is None:
        # If the document is not in our signature map, treat it as invalid
        return False

    # Use a constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sig, crypt_signature)