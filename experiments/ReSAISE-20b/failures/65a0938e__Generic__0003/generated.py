import urllib.request
from urllib.error import HTTPError, URLError

# Global mapping of document URLs to their correct cryptographic signatures
DOCUMENT_SIGNATURES = {
    # Example entries; in a real system these would be securely stored
    "https://example.com/doc1.pdf": "a3f5c7e9b1d2...",
    "https://example.com/doc2.pdf": "f4a8e6c3b9d1...",
    # Add more entries as needed
}

def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Validate a document's cryptographic signature.

    Parameters
    ----------
    doc_link : str
        URL of the document to validate.
    check_signature : str
        Cryptographic signature provided for verification.

    Returns
    -------
    bool
        True if the provided signature matches the stored signature, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed (e.g., 404 Not Found or network error).
    """
    # Verify the document exists by attempting a HEAD request
    try:
        req = urllib.request.Request(doc_link, method="HEAD")
        with urllib.request.urlopen(req) as resp:
            if resp.status != 200:
                raise IOError(f"Document not found (HTTP {resp.status})")
    except HTTPError as e:
        # If the server returns a 404 or other error, raise IOError
        raise IOError(f"Document at {doc_link} cannot be accessed: {e}") from e
    except URLError as e:
        # Network-related errors also trigger an IOError
        raise IOError(f"Failed to reach {doc_link}: {e}") from e

    # Retrieve the stored signature
    expected_signature = DOCUMENT_SIGNATURES.get(doc_link)

    if expected_signature is None:
        # If we have no record for this document, treat it as invalid
        return False

    # Compare signatures in a timing-attack resistant manner if possible
    # For simplicity, we use constant-time comparison from hmac
    import hmac
    return hmac.compare_digest(check_signature, expected_signature)