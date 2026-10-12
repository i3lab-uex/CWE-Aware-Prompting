import requests
from urllib.parse import urlparse

# Example pre‑defined dictionary mapping document URLs to their valid signatures.
DOCUMENT_SIGNATURES = {
    # 'https://example.com/doc1.pdf': 'signature_of_doc1',
    # Add actual URL:signature pairs here.
}

def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate the integrity of a remote document by checking its cryptographic signature.

    Parameters
    ----------
    document_location : str
        URL of the remote document to validate.
    crypto_sign : str
        Cryptographic signature provided for validation.

    Returns
    -------
    bool
        True if the signature matches the stored value, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Ensure we can reach the document
    try:
        response = requests.head(document_location, allow_redirects=True, timeout=10)
        if response.status_code != 200:
            raise IOError(f"Unable to retrieve document: HTTP {response.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Unable to retrieve document: {exc}") from exc

    # Normalize the URL for dictionary lookup
    normalized_url = _normalize_url(document_location)

    # Fetch expected signature from the dictionary (case‑insensitive key match)
    expected_sig = DOCUMENT_SIGNATURES.get(normalized_url)

    # If we don't have a stored signature, consider it invalid
    if expected_sig is None:
        return False

    # Compare signatures securely (constant‑time comparison)
    return _constant_time_compare(expected_sig, crypto_sign)


def _normalize_url(url: str) -> str:
    """
    Normalize a URL for dictionary lookup by removing fragments and standardizing the scheme.
    """
    parsed = urlparse(url)
    # Reconstruct URL without fragment
    return f"{parsed.scheme.lower()}://{parsed.netloc}{parsed.path}"


def _constant_time_compare(a: str, b: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode(), b.encode()):
        result |= x ^ y
    return result == 0