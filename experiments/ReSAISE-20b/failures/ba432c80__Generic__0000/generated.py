import requests
from urllib.parse import urlparse

# Global mapping of document URLs to their expected signatures.
DOC_SIGS = {
    # Example entries:
    # "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
    # "https://example.com/doc2.pdf": "1234567890abcdef",
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that the provided signature matches the expected value for
    the document located at *url*.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    sign_hash : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at *url* cannot be accessed (network error,
        non‑200 status code, etc.).
    """
    # First ensure the URL is valid
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise IOError(f"Invalid URL: {url}")

    # Try to access the document. A HEAD request is enough for
    # existence checks and is cheaper than GET.
    try:
        resp = requests.head(url, allow_redirects=True, timeout=10)
        if resp.status_code != 200:
            raise IOError(f"Document inaccessible, status code {resp.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Could not access document at {url}: {exc}") from exc

    # Retrieve the expected signature for this URL
    expected_sig = DOC_SIGS.get(url)
    if expected_sig is None:
        # If we don't have a signature for this URL, treat it as invalid
        return False

    # Perform a constant‑time comparison to mitigate timing attacks.
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _constant_time_compare(sign_hash, expected_sig)