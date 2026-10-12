import requests
from urllib.parse import urlparse

# Example global dictionary; in real use this should be populated securely.
DOC_SIGNATURES = {
    # 'https://example.com/docs/report.pdf': 'a1b2c3d4e5f6...',
    # Add real URL:signature pairs here.
}

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
        True if the provided signature matches the expected value for the
        document, False otherwise.

    Raises
    ------
    IOError
        If the document at ``file_url`` is inaccessible (e.g., network error,
        non-200 status code).
    """
    # Normalise URL (remove fragment, query parameters are ignored for lookup)
    parsed = urlparse(file_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    # Check that the URL is reachable
    try:
        response = requests.head(base_url, allow_redirects=True, timeout=5)
        if response.status_code != 200:
            raise IOError(f"Document not accessible: HTTP {response.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Unable to reach document at {file_url}") from exc

    # Retrieve expected signature
    expected_sig = DOC_SIGNATURES.get(base_url)

    if expected_sig is None:
        # If we don't have a signature for this URL, consider it invalid
        return False

    # Perform a constant‑time comparison to avoid timing attacks
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _constant_time_compare(sign, expected_sig)