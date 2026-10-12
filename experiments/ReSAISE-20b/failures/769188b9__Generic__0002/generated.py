import hashlib
from urllib.parse import urlparse

try:
    # use requests if available; fall back to urllib
    import requests  # type: ignore
except ImportError:
    import urllib.request as _ur

# Global dictionary of expected signatures (hashes) for each document URL
DOC_HASHES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    # "https://example.com/doc2.pdf": "e99a18c428cb38d5f260853678922e03",
}


def _is_url_accessible(url: str) -> bool:
    """
    Internal helper to verify that a URL is reachable.
    Returns True if the request succeeds with status 200, otherwise False.
    """
    try:
        # Prefer requests for better timeout handling
        if 'requests' in globals():
            resp = requests.head(url, allow_redirects=True, timeout=5)
            return resp.status_code == 200
        else:
            with _ur.urlopen(url, timeout=5) as resp:
                return resp.status == 200
    except Exception:
        return False


def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Confirm that a document at *resource_url* is authentic by comparing the
    supplied *crypto_signature* with the expected value stored in DOC_HASHES.

    Parameters
    ----------
    resource_url : str
        The full URL of the document to validate.
    crypto_signature : str
        The cryptographic signature (e.g., MD5, SHA256 hex digest) submitted
        with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value; False otherwise.

    Raises
    ------
    IOError
        If the document at *resource_url* cannot be accessed.
    """
    # 1. Verify that the URL is reachable
    if not _is_url_accessible(resource_url):
        raise IOError(f"Document at {resource_url} is inaccessible")

    # 2. Retrieve the expected signature
    # Use a normalized URL as key (e.g., scheme+netloc+path)
    parsed = urlparse(resource_url)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    expected_signature = DOC_HASHES.get(normalized_url)

    if expected_signature is None:
        # If no entry exists, we cannot authenticate
        return False

    # 3. Compare the signatures in a constant‑time manner to avoid timing attacks
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _constant_time_compare(crypto_signature.lower(), expected_signature.lower())