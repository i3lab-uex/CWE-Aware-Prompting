import urllib.request
import urllib.error
import hmac

# Global dictionary that maps a document URL to its correct cryptographic signature.
DOCUMENT_SIGNATURES = {
    # Example entries
    "https://example.com/doc1.txt": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/doc2.txt": "e99a18c428cb38d5f260853678922e03",
    # Add more URLs and their signatures as needed
}


def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the stored
    signature for a document located at ``url``.

    Parameters
    ----------
    url : str
        The URL of the remote document.
    doc_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        ``True`` if the provided signature matches the stored one, otherwise
        ``False``.

    Raises
    ------
    IOError
        If the document at ``url`` cannot be retrieved (e.g., 404 or network
        failure).  The error message contains the HTTP status code and reason.
    """
    # First, ensure the document exists by issuing a HEAD request.  This
    # conserves bandwidth and also allows us to detect missing resources.
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req) as resp:
            if resp.status >= 400:
                raise IOError(f"Document not found: {url} (HTTP {resp.status})")
    except urllib.error.HTTPError as e:
        # Convert HTTP errors into IOError with a helpful message.
        raise IOError(f"Document not found: {url} (HTTP {e.code})") from e
    except urllib.error.URLError as e:
        # Network-related errors (DNS failure, timeout, etc.)
        raise IOError(f"Could not access document: {url} ({e.reason})") from e

    # Retrieve the expected signature for this URL.
    expected_sig = DOCUMENT_SIGNATURES.get(url)
    if expected_sig is None:
        # No signature known for this URL; treat as invalid.
        return False

    # Use constant‑time comparison to avoid timing attacks that could leak
    # information about the correct signature.
    return hmac.compare_digest(expected_sig, doc_signature)