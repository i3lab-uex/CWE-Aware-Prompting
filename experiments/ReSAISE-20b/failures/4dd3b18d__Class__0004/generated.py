import requests
from urllib.parse import urlparse
import hmac

# Global dictionary mapping document URLs to their expected signatures.
DOC_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "sha256:abcd1234...",
    # "https://example.org/report.docx": "sha256:efgh5678..."
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
        True if the supplied signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at `file_url` cannot be accessed (e.g., network error,
        non‑200 HTTP status, or unsupported URL scheme).
    """
    # Ensure the URL uses a safe protocol.
    parsed = urlparse(file_url)
    if parsed.scheme not in {"http", "https"}:
        raise IOError(f"Unsupported URL scheme: {parsed.scheme}")

    try:
        # Use a reasonable timeout to avoid hanging indefinitely.
        response = requests.get(file_url, timeout=10)
    except (requests.RequestException, ValueError) as exc:
        raise IOError(f"Failed to retrieve document: {exc}") from exc

    if response.status_code != 200:
        raise IOError(f"Document inaccessible, HTTP status {response.status_code}")

    # Retrieve the expected signature for this URL.
    expected_sign = DOC_SIGNATURES.get(file_url)
    if expected_sign is None:
        # If we have no record for this URL, consider it invalid.
        return False

    # Perform a constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(sign, expected_sign)