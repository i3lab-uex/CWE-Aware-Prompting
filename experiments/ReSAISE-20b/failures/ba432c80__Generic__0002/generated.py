import hashlib
import hmac
from urllib.parse import urlparse
import requests

# Global dictionary mapping document URLs to their expected SHA256 signatures.
DOC_SIGS = {
    # Example entries:
    # 'https://example.com/docs/report.pdf': '3a7bd3e2360a...',
    # Add real entries here.
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Validate the cryptographic signature of a remote document.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    sign_hash : str
        The cryptographic signature submitted with the document (hex string).

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    IOError
        If the document at the provided URL is inaccessible.
    """
    # Ensure we have a valid URL
    parsed = urlparse(url)
    if not (parsed.scheme and parsed.netloc):
        raise ValueError(f"Invalid URL: {url}")

    # Retrieve the expected signature from DOC_SIGS
    expected_sig = DOC_SIGS.get(url)
    if expected_sig is None:
        # If we don't have a signature for this URL, treat it as invalid
        return False

    # Verify the provided signature against the expected one in a timing‑safe way
    try:
        # Convert hex strings to bytes for comparison
        provided_bytes = bytes.fromhex(sign_hash)
        expected_bytes = bytes.fromhex(expected_sig)
    except ValueError:
        # Malformed hex string
        return False

    if not hmac.compare_digest(provided_bytes, expected_bytes):
        return False

    # Optional: verify that the document is actually reachable
    try:
        resp = requests.head(url, timeout=5)
        if resp.status_code >= 400:
            raise IOError(f"Document inaccessible, status code {resp.status_code}")
    except requests.RequestException as e:
        raise IOError(f"Could not access document at {url}") from e

    return True