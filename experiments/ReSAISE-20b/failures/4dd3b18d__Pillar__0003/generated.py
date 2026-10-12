import hashlib
import hmac
from urllib.parse import urlparse

try:
    # Prefer the requests library if available, otherwise fall back to urllib
    import requests
except ImportError:
    requests = None

# Global dictionary mapping document URLs (or their paths) to expected signatures
DOC_SIGNATURES = {
    # Example entries; replace with real data in production
    "https://example.com/docs/report.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/docs/summary.txt": "e99a18c428cb38d5f260853678922e03",
}

def _get_signature_for_url(url: str) -> str | None:
    """
    Retrieve the expected signature for a given URL from DOC_SIGNATURES.
    Supports full URLs and simple paths.
    """
    # Normalize the URL to ensure consistent key lookup
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return None
    # Use the full URL as key; fallback to path only if not found
    return DOC_SIGNATURES.get(url) or DOC_SIGNATURES.get(parsed.path)

def _is_url_accessible(url: str, timeout: float = 5.0) -> bool:
    """
    Perform a lightweight HEAD request to verify that the URL is reachable.
    Returns True if status code < 400, otherwise False.
    """
    try:
        if requests is not None:
            resp = requests.head(url, timeout=timeout, allow_redirects=True)
            return resp.status_code < 400
        else:
            # Fallback to urllib if requests is unavailable
            import urllib.request
            req = urllib.request.Request(url, method='HEAD')
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status < 400
    except Exception:
        return False

def validate_document(file_url: str, sign: str) -> bool:
    """
    Validate the cryptographic signature of a remote document.

    Parameters
    ----------
    file_url : str
        URL of the document to validate.
    sign : str
        Signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at the provided URL is inaccessible.
    """
    # Ensure the URL is reachable before checking signature
    if not _is_url_accessible(file_url):
        raise IOError(f"Unable to access document at {file_url}")

    expected_sig = _get_signature_for_url(file_url)
    if expected_sig is None:
        # No known signature for this document
        return False

    # Use constant‑time comparison to avoid timing attacks (CWE‑693)
    return hmac.compare_digest(sign, expected_sig)

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_url = "https://example.com/docs/report.pdf"
    test_sig = "5f4dcc3b5aa765d61d8327deb882cf99"
    try:
        result = validate_document(test_url, test_sig)
        print(f"Signature valid: {result}")
    except IOError as e:
        print(str(e))