import hashlib
from urllib.parse import urlparse

try:
    # Prefer the requests library for robust HTTP handling.
    import requests
except ImportError:  # pragma: no cover
    raise RuntimeError("The 'requests' library is required to validate remote files.")


# Pre‑defined mapping of URLs to their expected cryptographic signatures.
# In a real system this would be populated from a secure source (e.g., a signed manifest).
DOCUMENT_SIGNATURES = {
    # Example entry: "https://example.com/file.pdf": "5d41402abc4b2a76b9719d911017c592"
}


def _compute_signature(content: bytes) -> str:
    """
    Compute the MD5 signature of the given content.

    The algorithm can be replaced with a stronger hash (e.g., SHA‑256) if required.
    """
    return hashlib.md5(content).hexdigest()


def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate that a remote document matches its expected cryptographic signature.

    Parameters
    ----------
    url : str
        The URL of the document to retrieve.
    crypt_signature : str
        The signature supplied by the caller (hexadecimal string).

    Returns
    -------
    bool
        ``True`` if the supplied signature matches the stored one, otherwise ``False``.

    Raises
    ------
    IOError
        If the document cannot be fetched from the specified URL.
    """
    # Sanity check: Ensure the supplied signature is a hex string of expected length
    if not isinstance(crypt_signature, str) or len(crypt_signature) != 32:
        return False

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Failed to retrieve document from {url}") from exc

    content = response.content
    computed_sig = _compute_signature(content)

    # Look up the expected signature for this URL (if present)
    expected_sig = DOCUMENT_SIGNATURES.get(url)

    # If we have a stored signature, compare it; otherwise trust the supplied one.
    if expected_sig is not None:
        return computed_sig.lower() == expected_sig.lower()

    # No stored signature; fall back to checking the supplied signature against computed one
    return computed_sig.lower() == crypt_signature.lower()