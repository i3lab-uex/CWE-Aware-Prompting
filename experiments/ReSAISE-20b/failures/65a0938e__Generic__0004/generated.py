import urllib.request
import urllib.error
from urllib.parse import urlparse

# Global dictionary mapping document URLs to their expected signatures.
# In a real system this would be populated securely from a trusted source.
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "abc123...",
    # "https://example.com/doc2.txt": "def456...",
}

def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the signature supplied for a remote document matches the
    expected signature stored in DOCUMENT_SIGNATURES.

    Parameters
    ----------
    doc_link : str
        The absolute URL of the document to validate.
    check_signature : str
        The cryptographic signature supplied by the caller.

    Returns
    -------
    bool
        True if the supplied signature matches the stored one, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be fetched (e.g., HTTP 404 or network error).
    """
    # Validate the URL scheme – only allow http/https to prevent local file access.
    parsed = urlparse(doc_link)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Attempt to fetch the document; raise IOError on failure.
    try:
        with urllib.request.urlopen(doc_link, timeout=10) as resp:
            # We don't actually need the content for signature comparison,
            # but fetching ensures the document exists and is reachable.
            resp.read(1)  # read a byte to confirm retrieval
    except urllib.error.HTTPError as e:
        raise IOError(f"HTTP error when accessing {doc_link}: {e.code} {e.reason}") from e
    except urllib.error.URLError as e:
        raise IOError(f"URL error when accessing {doc_link}: {e.reason}") from e
    except Exception as e:
        raise IOError(f"Unexpected error when accessing {doc_link}: {e}") from e

    # Retrieve the expected signature for this document.
    expected_signature = DOCUMENT_SIGNATURES.get(doc_link)

    # If the URL is not present in our signature store, we treat it as invalid.
    if expected_signature is None:
        return False

    # Compare signatures in a timing‑attack resistant way.
    # Python 3.5+ provides hmac.compare_digest for this purpose.
    import hmac
    return hmac.compare_digest(check_signature, expected_signature)