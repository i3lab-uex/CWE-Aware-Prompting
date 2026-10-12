import requests
from hmac import compare_digest
from urllib.parse import urlparse

# Example global dictionary of expected signatures.
# In a real application this would be populated from a secure source.
DOC_HASHES = {
    # 'https://example.com/doc1.pdf': 'sha256:abcd1234...',
    # Add entries here.
}


def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    signature for a document hosted at ``resource_url``.

    Parameters
    ----------
    resource_url : str
        The URL of the document to validate.
    crypto_signature : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        ``True`` if the signature matches the expected value, otherwise
        ``False``.

    Raises
    ------
    IOError
        If the document at ``resource_url`` cannot be accessed (e.g. network
        error, non‑2xx status code).
    ValueError
        If ``resource_url`` is not a valid HTTP/HTTPS URL.
    """
    # Basic sanity checks
    if not isinstance(resource_url, str) or not isinstance(crypto_signature, str):
        raise TypeError("Both resource_url and crypto_signature must be strings")

    parsed = urlparse(resource_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("resource_url must use http or https scheme")

    # Verify that the URL is reachable.  We do not need to download the
    # entire document, just confirm that a GET request succeeds.
    try:
        resp = requests.head(resource_url, allow_redirects=True, timeout=5)
        if not resp.ok:
            raise IOError(f"Unable to access document at {resource_url}: "
                          f"{resp.status_code} {resp.reason}")
    except requests.RequestException as exc:
        raise IOError(f"Network error when accessing {resource_url}") from exc

    # Retrieve the expected signature for this URL
    expected = DOC_HASHES.get(resource_url)
    if expected is None:
        # No known signature for this URL – treat as invalid
        return False

    # Use constant‑time comparison to avoid timing attacks
    return compare_digest(expected, crypto_signature)