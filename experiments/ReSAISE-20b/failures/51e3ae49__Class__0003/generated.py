import hashlib
import hmac
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# Global dictionary containing correct signatures for known documents.
# Example: {'https://example.com/doc1.pdf': 'abcd1234...'}
DOCUMENT_SIGNATURES = {
    # Populate with actual URLs and their correct signatures.
}

def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Validate a document's integrity by comparing the provided cryptographic
    signature with the expected signature stored in DOCUMENT_SIGNATURES.

    Parameters:
        file_url (str): URL of the document to validate.
        crypt_signature (str): Signature provided for verification.

    Returns:
        bool: True if the signature matches; False otherwise.

    Raises:
        IOError: If the document cannot be retrieved (e.g., 404 or network error).
    """
    # Ensure we can fetch the document to confirm its existence
    try:
        req = Request(file_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            # Read the first few bytes just to trigger a network fetch.
            _ = response.read(1)
    except HTTPError as e:
        # 404 Not Found or other HTTP errors
        raise IOError(f"Document not found at {file_url}: {e.code}") from e
    except URLError as e:
        # Network-related errors (DNS failure, connection refused, etc.)
        raise IOError(f"Unable to access document at {file_url}: {e.reason}") from e

    # Retrieve the expected signature for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(file_url)
    if expected_sig is None:
        # If we have no stored signature, we cannot verify authenticity
        raise ValueError(f"No known signature for URL: {file_url}")

    # Compare signatures using a timing‑safe comparison
    return hmac.compare_digest(expected_sig, crypt_signature)