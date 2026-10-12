import requests
from urllib.parse import urlparse, urlunparse
import hmac

# Global dictionary mapping normalized URLs to expected signatures
DOC_HASHES = {
    # Example entries:
    # "https://example.com/docs/doc1.pdf": "abc123signature",
    # "https://example.org/files/report.pdf": "def456signature",
}

def _normalize_url(url: str) -> str:
    """
    Normalise a URL so that different but equivalent URLs map to the same key.
    This removes fragments and query parameters, sorts query params,
    and normalises the scheme/host to lowercase.
    """
    parsed = urlparse(url)
    # Ensure scheme and netloc are lowercased
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Sort query parameters alphabetically
    query = '&'.join(
        sorted(parsed.query.split('&')) if parsed.query else []
    )

    # Reconstruct the URL without fragment
    normalized = urlunparse((scheme, netloc, parsed.path, parsed.params,
                             query, ''))
    return normalized

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that the cryptographic signature of a remote document matches
    the expected value stored in DOC_HASHES.

    Parameters
    ----------
    resource_url : str
        The URL of the document to validate.
    crypto_signature : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    IOError
        If the document at `resource_url` cannot be accessed (network error,
        non-200 status code, etc.).
    """
    # First, check that the document is reachable
    try:
        resp = requests.head(resource_url, allow_redirects=True, timeout=5)
        if resp.status_code != 200:
            raise IOError(f"Unable to access document: HTTP {resp.status_code}")
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Unable to access document: {exc}") from exc

    # Normalise the URL for lookup
    normalized_url = _normalize_url(resource_url)

    expected_sig = DOC_HASHES.get(normalized_url)
    if expected_sig is None:
        # No known signature for this URL – treat as invalid
        return False

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_sig, crypto_signature)