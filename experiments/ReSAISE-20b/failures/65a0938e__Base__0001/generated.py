import urllib.request
from urllib.error import HTTPError, URLError
import hmac

# Example global mapping of document URLs to their correct signatures.
# In a real system this would be securely stored and possibly refreshed
# from a trusted source.  Here we just provide a placeholder.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "f2c9d6b3e8a7c4f0",
    "https://example.com/doc2.pdf": "9b1d8a4e3f6c7b0a",
    # Add more entries as needed
}

def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a remote document.

    Parameters
    ----------
    doc_link : str
        URL of the document to validate.
    check_signature : str
        Cryptographic signature provided for verification.

    Returns
    -------
    bool
        True if the signature matches, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved (e.g., 404 Not Found).
    """
    # Ensure we can reach the document
    try:
        with urllib.request.urlopen(doc_link, timeout=10) as response:
            # If we get a 200 OK, continue. Any other status will raise HTTPError.
            if response.status != 200:
                raise IOError(f"Unexpected HTTP status {response.status} for {doc_link}")
    except HTTPError as e:
        if e.code == 404:
            raise IOError(f"Document not found: {doc_link}") from None
        else:
            raise IOError(f"HTTP error {e.code} for {doc_link}") from None
    except URLError as e:
        raise IOError(f"Unable to reach {doc_link}: {e}") from None

    # Retrieve the expected signature
    expected_signature = DOCUMENT_SIGNATURES.get(doc_link)
    if expected_signature is None:
        # If the document exists but we have no stored signature, consider it invalid
        return False

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(check_signature, expected_signature)