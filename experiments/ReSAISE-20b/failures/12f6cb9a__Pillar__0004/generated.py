import urllib.request
import urllib.error
from urllib.parse import urlparse, urlunparse
import hmac

# Global dictionary containing the correct signatures for known documents.
# Example: {"https://example.com/doc1.pdf": "abc123", ...}
DOCUMENT_SIGNATURES = {
    # Populate with actual signatures in real usage
}

def _canonical_url(url: str) -> str:
    """
    Normalise the URL to a canonical form so that different
    but equivalent URLs map to the same key in DOCUMENT_SIGNATURES.
    """
    parsed = urlparse(url)
    # Lowercase scheme and host, strip default ports
    netloc = parsed.netloc.lower()
    if (parsed.scheme == 'http' and parsed.port == 80) or \
       (parsed.scheme == 'https' and parsed.port == 443):
        netloc = parsed.hostname.lower()
    canonical = urlunparse((
        parsed.scheme.lower(),
        netloc,
        parsed.path or '',
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    return canonical

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the
    stored signature for a remote document.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    doc_signature : str
        The cryptographic signature provided for verification.

    Returns
    -------
    bool
        True if the supplied signature matches the stored one,
        False otherwise.

    Raises
    ------
    IOError
        If the document at the specified URL cannot be found or
        accessed (e.g., HTTP 404, network error).
    """
    # Normalise URL to match the key format in DOCUMENT_SIGNATURES
    canonical = _canonical_url(url)

    # Check that we have a known document signature
    if canonical not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document at {url} not found in signature registry")

    # Attempt to fetch the document to ensure it is reachable
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            if resp.status >= 400:
                raise IOError(f"Failed to retrieve document: HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        raise IOError(f"HTTP error retrieving document: {e.code}") from e
    except urllib.error.URLError as e:
        raise IOError(f"URL error retrieving document: {e.reason}") from e

    # Retrieve the expected signature
    expected_sig = DOCUMENT_SIGNATURES[canonical]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(doc_signature, expected_sig)