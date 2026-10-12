import requests
import hmac
from urllib.parse import urlparse

# Example global dictionary of expected signatures for documents.
# Keys are the full URL strings, values are the corresponding cryptographic signatures.
DOC_SIGNATURES = {
    # 'https://example.com/documents/report.pdf': 'abcd1234...',
    # Add entries as needed.
}

def validate_document(file_url: str, sign: str) -> bool:
    """
    Validate the cryptographic signature of a document located at `file_url`.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    sign : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the provided signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at `file_url` is inaccessible (network error, 404, etc.).
    """
    # Ensure the URL can be reached – this is a lightweight HEAD request
    try:
        response = requests.head(file_url, allow_redirects=True, timeout=5)
        if not response.ok:
            raise IOError(f"Unable to access document: HTTP {response.status_code}")
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Unable to access document: {exc}") from exc

    # Retrieve the expected signature for this URL
    expected = DOC_SIGNATURES.get(file_url)
    if expected is None:
        # No signature stored for this URL – treat as invalid
        return False

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected)