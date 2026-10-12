import requests
import hmac
from urllib.parse import urlparse, urlunparse

# Global dictionary mapping canonical URLs to their expected signatures
DOC_SIGNATURES = {
    # Example entries (URL : signature)
    "https://example.com/docs/report.pdf": "a1b2c3d4e5f6g7h8i9j0",
    # Add more entries as needed
}

def _canonical_url(url: str) -> str:
    """
    Normalise a URL for lookup in DOC_SIGNATURES.
    This removes fragments and ensures consistent scheme/host formatting.
    """
    parsed = urlparse(url)
    # Remove fragment and query for canonical form
    return urlunparse((parsed.scheme, parsed.netloc.lower(), parsed.path,
                       '', '', ''))

def validate_document(file_url: str, sign: str) -> bool:
    """
    Validate the cryptographic signature of a remote document.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    sign : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at the provided URL is inaccessible (HTTP error or network issue).
    """
    # Check that we can reach the document
    try:
        head_resp = requests.head(file_url, allow_redirects=True, timeout=5)
        if not head_resp.ok:
            # Treat non-success status codes as inaccessible
            raise IOError(f"Document not accessible: {file_url} (status {head_resp.status_code})")
    except requests.RequestException as exc:
        raise IOError(f"Failed to access document at {file_url}") from exc

    # Canonicalise URL for lookup
    canon_url = _canonical_url(file_url)

    expected_sig = DOC_SIGNATURES.get(canon_url)
    if expected_sig is None:
        # If we have no record for this URL, treat as invalid
        return False

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected_sig)