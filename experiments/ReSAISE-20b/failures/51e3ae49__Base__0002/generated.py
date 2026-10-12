import urllib.request
import urllib.error
import hmac

# Example global dictionary mapping URLs to their correct signatures.
# In a real system this would be populated from a secure source.
DOCUMENT_SIGNATURES = {
    # 'https://example.com/doc1.pdf': 'abc123...',
    # ...
}


def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the one
    stored for the document at `file_url`.

    Args:
        file_url (str): URL of the remote document.
        crypt_signature (str): Signature supplied for verification.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved (e.g., 404 or network error).
    """
    # Verify that the URL is present in our trusted signatures list.
    if file_url not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document '{file_url}' not found or not trusted.")

    # Attempt to fetch the document to ensure it exists.
    try:
        with urllib.request.urlopen(file_url) as response:
            # We don't actually need the content for signature verification,
            # but we read a small amount to confirm accessibility.
            response.read(1)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise IOError(f"Document '{file_url}' not found (HTTP 404).")
        else:
            raise IOError(f"Error accessing document '{file_url}': {e}") from e
    except urllib.error.URLError as e:
        raise IOError(f"Network error accessing document '{file_url}': {e}") from e

    # Retrieve the expected signature for this URL.
    expected_signature = DOCUMENT_SIGNATURES[file_url]

    # Use constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(expected_signature, crypt_signature)