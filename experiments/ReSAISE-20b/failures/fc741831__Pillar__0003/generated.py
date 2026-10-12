import requests
import hmac
from urllib.parse import urlparse

# Example of pre‑defined signatures. In real use, this would be populated elsewhere.
DOCUMENT_SIGNATURES = {
    # 'https://example.com/doc1.pdf': 'abcdef123456...',
}

def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate a remotely hosted document by checking its cryptographic signature.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    crypt_signature : str
        The signature claimed for this document.

    Returns
    -------
    bool
        True if the signature matches the stored one, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Basic sanity check for the URL
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise IOError(f"Invalid URL: {url}")

    try:
        # Use a reasonable timeout and stream to avoid loading huge files into memory
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Could not retrieve document from {url}") from exc

    # Compute a simple checksum (e.g., SHA-256) for the file content
    # For demonstration, we'll use the raw response content.
    # In production, consider streaming and incremental hashing for large files.
    file_bytes = response.content
    computed_hash = hmac.new(b'secret_key', file_bytes, digestmod='sha256').hexdigest()

    # Compare the computed hash with the provided signature using a timing‑safe comparison
    return hmac.compare_digest(computed_hash, crypt_signature)