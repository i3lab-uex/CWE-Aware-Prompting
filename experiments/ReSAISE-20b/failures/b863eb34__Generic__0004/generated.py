import hashlib
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Example mapping of URLs to their expected SHA‑256 signatures.
# In a real system this would be populated from a secure source.
DOCUMENT_SIGNATURES = {
    # 'https://example.com/doc1.pdf': '3a7bd3e2360...'
}

def _download_document(url: str) -> bytes:
    """
    Download the document from the given URL.
    Raises IOError if the request fails for any reason.
    """
    try:
        req = Request(url, headers={'User-Agent': 'verify-document/1.0'})
        with urlopen(req, timeout=10) as resp:
            return resp.read()
    except (HTTPError, URLError) as exc:
        raise IOError(f"Could not access document at {url}") from exc

def _compute_signature(data: bytes) -> str:
    """
    Compute the SHA‑256 hash of the document data.
    Returns the hex digest string.
    """
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the document at `doc_url` has a signature matching
    the one stored in DOCUMENT_SIGNATURES.

    Parameters:
        doc_url (str): URL of the document to verify.
        signature (str): Cryptographic signature provided for the document.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        IOError: If the document cannot be accessed.
    """
    # Fetch the document
    data = _download_document(doc_url)

    # Compute its signature locally
    local_sig = _compute_signature(data)

    # Retrieve the expected signature from the global mapping
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)

    # If we have no stored signature, consider it invalid
    if expected_sig is None:
        return False

    # Compare the computed signature with the provided one and the expected
    if local_sig != signature:
        return False

    # Optionally, ensure that the provided signature matches the stored one
    return local_sig == expected_sig