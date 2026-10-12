import requests
from urllib.parse import urlparse

# Global dictionary mapping document URLs to their expected signatures.
DOC_SIGNATURES = {
    # Example entries
    "https://example.com/doc1.pdf": "abc123",
    "https://example.org/report.docx": "def456",
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
        True if the provided signature matches the expected value,
        False otherwise.

    Raises
    ------
    IOError
        If the document at `file_url` cannot be accessed.
    """
    # Basic URL validation
    parsed = urlparse(file_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {file_url}")

    # Check that the document is reachable.
    try:
        # Use a HEAD request to minimize bandwidth; fallback to GET if HEAD fails
        resp = requests.head(file_url, timeout=5)
        if resp.status_code >= 400:
            # HEAD may not be supported; try GET
            resp = requests.get(file_url, stream=True, timeout=5)
        resp.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Unable to access document at {file_url}") from exc

    # Retrieve the expected signature for this URL.
    expected_sign = DOC_SIGNATURES.get(file_url)
    if expected_sign is None:
        # If the URL isn't in our whitelist, treat it as an invalid document.
        return False

    # Compare signatures safely to avoid timing attacks.
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _constant_time_compare(sign, expected_sign)