import hashlib
from urllib.parse import urlparse

try:
    # Prefer the lightweight `httpx` if available, otherwise fall back to `requests`
    import httpx
    _Client = httpx.Client
except ImportError:
    import requests
    _Client = requests.Session

# Pre‑defined mapping of document URLs to their expected SHA256 signatures.
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "5e884898da28047151d0e56f8dc6292773603...",
    # "https://example.com/doc2.txt": "b94d27b9934d3e08a52e52d7da7dabfa...",
}

def _fetch_content(url: str) -> bytes:
    """
    Retrieve the raw content from a URL. Raises IOError on failure.
    """
    try:
        with _Client() as client:
            response = client.get(url, timeout=10)
            response.raise_for_status()
            return response.content
    except Exception as exc:
        raise IOError(f"Unable to fetch document from {url}") from exc

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate that the cryptographic signature of a remote document matches
    the known, trusted value.

    Parameters:
        location (str): URL of the document to verify.
        sign (str): SHA256 hexadecimal digest supplied by the caller.

    Returns:
        bool: True if the signature is correct, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved.
    """
    # Normalise the URL (e.g., strip fragments) so dictionary lookup works
    parsed = urlparse(location)
    normalised_url = parsed._replace(fragment="").geturl()

    # Fetch the document content
    content = _fetch_content(normalised_url)

    # Compute SHA256 digest of the fetched content
    computed_digest = hashlib.sha256(content).hexdigest()

    # Retrieve the trusted signature for this URL
    expected_digest = DOCUMENT_SIGNATURES.get(normalised_url)

    # If we have no stored signature for this URL, treat it as a failure
    if expected_digest is None:
        return False

    # Compare all three digests: supplied, computed and expected
    return sign.lower() == computed_digest == expected_digest.lower()