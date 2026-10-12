import urllib.request
import urllib.error
import hmac

# Global dictionary mapping document URLs to their correct signatures.
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "a1b2c3d4e5f6...",
    # "https://example.com/doc2.txt": "deadbeef1234..."
}

def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the stored
    signature for a remote document.

    Parameters
    ----------
    file_url : str
        URL of the document to validate.
    crypt_signature : str
        Signature supplied for verification.

    Returns
    -------
    bool
        True if the signature matches the stored one, False otherwise.

    Raises
    ------
    IOError
        If the document at ``file_url`` cannot be retrieved.
    """
    # Ensure we can reach the URL; this also protects against typos in the key.
    try:
        with urllib.request.urlopen(file_url) as response:
            # We don't actually need the content for signature comparison,
            # but we still fetch it to guarantee the URL is valid.
            _ = response.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise IOError(f"Document not found: {file_url}") from e
        else:
            raise IOError(f"Error accessing document {file_url}: {e}") from e
    except urllib.error.URLError as e:
        raise IOError(f"Could not reach {file_url}: {e}") from e

    # Retrieve the stored signature for this URL.
    expected_sig = DOCUMENT_SIGNATURES.get(file_url)
    if expected_sig is None:
        # URL not registered; treat as invalid.
        return False

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sig, crypt_signature)