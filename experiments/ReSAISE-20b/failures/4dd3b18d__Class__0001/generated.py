import requests
from urllib.parse import urlparse
import hmac

# Global dictionary mapping document URLs to their expected signatures.
# Example:
# DOC_SIGNATURES = {
#     "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
#     "https://example.com/doc2.pdf": "e99a18c428cb38d5f260853678922e03",
# }
DOC_SIGNATURES = {}

def validate_document(file_url: str, sign: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    signature for a document located at `file_url`.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    sign : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    IOError
        If the document at `file_url` is inaccessible (network error,
        non‑200 status code, etc.).
    """
    # Basic URL validation
    parsed = urlparse(file_url)
    if not (parsed.scheme and parsed.netloc):
        raise IOError(f"Invalid URL: {file_url}")

    # Ensure the document is reachable before verifying its signature.
    try:
        response = requests.head(file_url, timeout=5)
        if response.status_code != 200:
            raise IOError(f"Document not accessible, status code {response.status_code}")
    except (requests.RequestException, ValueError) as exc:
        raise IOError(f"Could not access document at {file_url}") from exc

    # Retrieve the expected signature for this URL
    expected_sig = DOC_SIGNATURES.get(file_url)
    if expected_sig is None:
        # If we have no record of this document, treat it as invalid
        return False

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_sig, sign)