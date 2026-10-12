import urllib.request
import urllib.error
import hmac

# Global dictionary mapping document URLs to their correct signatures
DOCUMENT_SIGNATURES = {
    # Example entries (replace with real values)
    "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/doc2.pdf": "e99a18c428cb38d5f260853678922e03",
    # Add more entries as needed
}


def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the stored
    signature for a document located at `doc_link`.

    Parameters
    ----------
    doc_link : str
        URL of the document to validate.
    check_signature : str
        Cryptographic signature provided for verification.

    Returns
    -------
    bool
        True if the supplied signature matches the stored signature,
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved (e.g., 404 Not Found).
    """
    # First, attempt to retrieve the document to confirm its existence.
    try:
        with urllib.request.urlopen(doc_link) as response:
            # We don't actually need the content; just confirm that we can access it.
            if response.status != 200:
                raise IOError(f"Failed to retrieve document: HTTP {response.status}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise IOError(f"Document not found at {doc_link}") from None
        else:
            raise IOError(f"HTTP error while accessing document: {e.code}") from None
    except urllib.error.URLError as e:
        raise IOError(f"Could not reach the document URL: {e.reason}") from None

    # Retrieve the expected signature from the global mapping.
    expected_sig = DOCUMENT_SIGNATURES.get(doc_link)
    if expected_sig is None:
        # If we don't have a stored signature for this document, treat it as invalid.
        return False

    # Use hmac.compare_digest to avoid timing attacks (CWE-693).
    return hmac.compare_digest(expected_sig, check_signature)