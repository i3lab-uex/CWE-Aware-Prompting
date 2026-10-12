import hashlib
import urllib.request
from urllib.error import HTTPError, URLError

# Global dictionary mapping document URLs to their expected SHA‑256 signatures
DOCUMENT_SIGNATURES = {
    # Example entries (URL: signature)
    # "https://example.com/doc1.pdf": "a3b2c4... (hex)",
    # "https://example.com/doc2.txt": "f1e0d8... (hex)",
}

def _compute_sha256(data: bytes) -> str:
    """Return the SHA‑256 hexadecimal digest of the given data."""
    return hashlib.sha256(data).hexdigest()


def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Verify that the document located at *file_url* has a SHA‑256 signature
    matching *crypt_signature*.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    crypt_signature : str
        The provided cryptographic signature (hexadecimal string).

    Returns
    -------
    bool
        True if the computed signature matches the expected one; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved (e.g., 404 Not Found or network error).
    """
    # Ensure the URL is known in our signature store
    if file_url not in DOCUMENT_SIGNATURES:
        raise IOError(f"Unknown document URL: {file_url}")

    expected_sig = DOCUMENT_SIGNATURES[file_url].lower()
    provided_sig = crypt_signature.lower()

    try:
        # Retrieve the document with a reasonable timeout
        with urllib.request.urlopen(file_url, timeout=10) as resp:
            if resp.status != 200:
                raise IOError(f"Failed to fetch document: HTTP {resp.status}")
            data = resp.read()
    except (HTTPError, URLError) as exc:
        raise IOError(f"Unable to retrieve document at {file_url}") from exc

    # Compute the actual SHA‑256 signature
    computed_sig = _compute_sha256(data)

    # Constant-time comparison to avoid timing attacks
    if len(computed_sig) != len(expected_sig):
        return False

    result = 0
    for x, y in zip(computed_sig.encode(), expected_sig.encode()):
        result |= x ^ y

    return result == 0