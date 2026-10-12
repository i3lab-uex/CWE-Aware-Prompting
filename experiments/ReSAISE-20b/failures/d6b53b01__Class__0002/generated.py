import hashlib
import requests

# Pre‑defined mapping of document URLs to their valid signatures.
# In a real system this would be stored securely and not hard‑coded.
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "a3f5c8e9...",
    # "https://example.com/doc2.pdf": "b7d4a1c2...",
}

def _compute_signature(content: bytes) -> str:
    """
    Compute a deterministic signature for the given content.
    For demonstration we use SHA-256 hex digest; replace with
    proper cryptographic signing in production.
    """
    return hashlib.sha256(content).hexdigest()


def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document.

    Parameters
    ----------
    document_location : str
        URL pointing to the target document.
    crypto_sign : str
        Expected cryptographic signature for the document.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the provided URL.
    """
    try:
        # Retrieve the document with a reasonable timeout.
        resp = requests.get(document_location, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Convert any network/HTTP error into IOError for the caller.
        raise IOError(f"Failed to retrieve document: {exc}") from exc

    # Compute the signature of the retrieved content.
    actual_signature = _compute_signature(resp.content)

    # Compare signatures in a constant‑time manner to mitigate timing attacks.
    return hashlib.compare_digest(actual_signature, crypto_sign)