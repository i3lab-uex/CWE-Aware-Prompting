import urllib.request
import urllib.error
import hmac

# Global dictionary mapping URLs to their correct cryptographic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries; in a real system these would be securely stored and managed.
    "https://example.com/doc1.pdf": "a3f5c2b7e8d9...",
    "https://example.com/doc2.pdf": "4c1e6f8a9b0d...",
    # ... add more entries as needed ...
}

def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Validate the integrity of a remote document by checking its cryptographic signature.

    Args:
        file_url (str): URL of the document to validate.
        crypt_signature (str): Signature provided for verification.

    Returns:
        bool: True if the signature matches the stored signature, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved (e.g., 404 Not Found).
    """
    # Attempt to fetch the document to confirm it exists.
    try:
        with urllib.request.urlopen(file_url) as response:
            # Read a small amount to ensure the request succeeded.
            _ = response.read(1)
    except urllib.error.HTTPError as e:
        # HTTP 404 (Not Found) or other errors trigger an IOError.
        raise IOError(f"Document not found at {file_url}: HTTP {e.code}") from e
    except urllib.error.URLError as e:
        # Network-related errors.
        raise IOError(f"Failed to access {file_url}: {e.reason}") from e

    # Retrieve the expected signature for this URL.
    expected_sig = DOCUMENT_SIGNATURES.get(file_url)
    if expected_sig is None:
        # If no signature is stored, we cannot validate.
        return False

    # Perform a constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(crypt_signature, expected_sig)