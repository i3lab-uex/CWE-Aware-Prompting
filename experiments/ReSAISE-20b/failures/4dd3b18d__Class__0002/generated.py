import hashlib
import urllib.parse
from typing import Dict

# Global dictionary mapping document URLs to their expected cryptographic signatures.
DOC_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real data in production
    "https://example.com/docs/report.pdf": "a3b5c7d9e1f2...",
    "https://example.com/docs/summary.pdf": "4b6c8d0e2f3a...",
}

def _fetch_document(url: str) -> bytes:
    """
    Retrieve the raw content of a document from the given URL.
    Raises an IOError if the request fails or the status code is not 200.
    """
    import requests

    # Ensure HTTPS for secure transfer
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        raise IOError(f"Insecure or unsupported URL scheme: {parsed.scheme}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as exc:
        raise IOError(f"Unable to fetch document from {url}: {exc}") from exc

    return response.content


def _compute_signature(data: bytes) -> str:
    """
    Compute a SHA-256 hash of the document data and return it as a hex string.
    """
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()


def validate_document(file_url: str, sign: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the expected
    signature for the document located at `file_url`.

    Parameters:
        file_url (str): The HTTPS URL of the document to validate.
        sign (str):   The cryptographic signature submitted with the document.

    Returns:
        bool: True if the signature matches the expected value, False otherwise.

    Raises:
        IOError: If the document at `file_url` is inaccessible or cannot be fetched.
    """
    # Fetch the remote document
    content = _fetch_document(file_url)

    # Compute the signature locally
    expected_signature = _compute_signature(content)

    # Compare signatures in a timing‑attack resistant manner
    import hmac
    return hmac.compare_digest(expected_signature, sign)