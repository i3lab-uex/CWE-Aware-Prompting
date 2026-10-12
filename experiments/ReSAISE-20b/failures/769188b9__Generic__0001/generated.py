import requests
from typing import Dict

# Global dictionary that maps a document URL to its expected cryptographic signature.
DOC_HASHES: Dict[str, str] = {
    # Example entries – replace with real data in production.
    "https://example.com/doc1.pdf": "sha256:abcd1234...",
    "https://example.org/report.xml": "sha256:efgh5678..."
}


def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Validate that a cryptographic signature matches the expected value for a document
    hosted at ``resource_url``.

    Parameters
    ----------
    resource_url : str
        The URL of the document to validate.
    crypto_signature : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        ``True`` if the provided signature matches the expected value for the document,
        otherwise ``False``.

    Raises
    ------
    IOError
        If the document at the provided URL is inaccessible (e.g., network error,
        non‑200 HTTP status, or timeout).
    """
    # 1. Verify that the URL is known in DOC_HASHES
    expected_sig = DOC_HASHES.get(resource_url)
    if expected_sig is None:
        # Unknown document – treat as a signature mismatch
        return False

    # 2. Check that the remote document is reachable.
    try:
        response = requests.head(resource_url, allow_redirects=True, timeout=10)
        if response.status_code != 200:
            raise IOError(f"Document not accessible: HTTP {response.status_code}")
    except requests.RequestException as exc:
        # Wrap any request‑related exception into an IOError
        raise IOError(f"Could not reach document at {resource_url}") from exc

    # 3. Compare signatures in a constant‑time manner to avoid timing attacks.
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode("utf-8"), b.encode("utf-8")):
            result |= x ^ y
        return result == 0

    return _constant_time_compare(crypto_signature, expected_sig)