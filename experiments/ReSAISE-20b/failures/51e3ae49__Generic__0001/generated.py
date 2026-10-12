import urllib.request
import urllib.error
import hmac

# Global dictionary mapping document URLs to their correct cryptographic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries
    "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/doc2.pdf": "e99a18c428cb38d5f260853678922e03",
    # Add more entries as needed
}


def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the expected
    signature for the document located at `file_url`.

    Parameters
    ----------
    file_url : str
        URL of the remote document to validate.
    crypt_signature : str
        Cryptographic signature provided for verification.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed (e.g., 404 Not Found or network error).
    """
    # Ensure the URL is reachable before attempting signature verification.
    try:
        with urllib.request.urlopen(file_url, timeout=10) as response:
            # We only need to check that the URL is reachable.
            if response.status != 200:
                raise IOError(f"Document not found or inaccessible: {file_url}")
    except urllib.error.HTTPError as e:
        raise IOError(f"HTTP error accessing document {file_url}: {e}") from None
    except urllib.error.URLError as e:
        raise IOError(f"URL error accessing document {file_url}: {e}") from None

    # Retrieve the expected signature for this URL.
    expected_signature = DOCUMENT_SIGNATURES.get(file_url)
    if expected_signature is None:
        # No signature stored for this URL.
        return False

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_signature, crypt_signature)