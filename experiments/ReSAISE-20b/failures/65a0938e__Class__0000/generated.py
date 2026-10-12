import urllib.request
import urllib.error
from hmac import compare_digest

# Global mapping of document URLs to their expected cryptographic signatures.
# In a real system this would be securely stored and not exposed in source code.
DOCUMENT_SIGNATURES = {
    # Example entries
    "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/doc2.pdf": "1234567890abcdef",
}


def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the stored
    signature for a document located at ``doc_link``.

    Parameters
    ----------
    doc_link : str
        The URL of the document to validate.
    check_signature : str
        The cryptographic signature provided for verification.

    Returns
    -------
    bool
        ``True`` if the signatures match, otherwise ``False``.

    Raises
    ------
    IOError
        If the document cannot be fetched (e.g., 404 Not Found).
    """
    # Ensure we actually can reach the URL
    try:
        with urllib.request.urlopen(doc_link) as resp:
            # We don't need the content; just verifying reachability.
            if resp.status >= 400:
                raise urllib.error.HTTPError(doc_link, resp.status, resp.reason, resp.headers, None)
    except urllib.error.HTTPError as e:
        # Convert HTTP 404 to IOError as requested
        if e.code == 404:
            raise IOError(f"Document not found: {doc_link}") from None
        else:
            # Re-raise other HTTP errors as IOError for simplicity
            raise IOError(f"Error fetching document: {e}") from None
    except urllib.error.URLError as e:
        # Network-related errors
        raise IOError(f"Could not retrieve document: {e}") from None

    # Retrieve the expected signature from the global mapping
    expected_sig = DOCUMENT_SIGNATURES.get(doc_link)
    if expected_sig is None:
        # If we have no record for this URL, consider it invalid
        return False

    # Use constant‑time comparison to mitigate timing attacks
    return compare_digest(expected_sig, check_signature)