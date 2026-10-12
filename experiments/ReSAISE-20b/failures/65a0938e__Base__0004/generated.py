import urllib.request
import urllib.error
import hmac

# Example global mapping of document URLs to their correct signatures.
# In a real system this would be securely stored and protected.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/doc2.pdf": "e99a18c428cb38d5f260853678922e03",
    # Add more URLs and signatures as needed.
}


def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a document at `doc_link`.

    Parameters
    ----------
    doc_link : str
        The URL of the document to validate.
    check_signature : str
        The cryptographic signature that is provided for verification.

    Returns
    -------
    bool
        True if the signature matches, False otherwise.

    Raises
    ------
    IOError
        If the document at `doc_link` cannot be found (HTTP 404 or network error).
    """
    # First ensure the document exists by performing a HEAD request.
    try:
        req = urllib.request.Request(doc_link, method="HEAD")
        with urllib.request.urlopen(req) as resp:
            if resp.status != 200:
                raise IOError(f"Document not found (HTTP {resp.status})")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise IOError(f"Document not found: {doc_link}") from e
        else:
            raise IOError(f"Error accessing document: {e}") from e
    except urllib.error.URLError as e:
        raise IOError(f"Network error while accessing document: {e}") from e

    # Retrieve the expected signature from the global mapping.
    expected_sig = DOCUMENT_SIGNATURES.get(doc_link)
    if expected_sig is None:
        # If we don't have a stored signature for this URL, treat it as invalid.
        return False

    # Use constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(check_signature, expected_sig)