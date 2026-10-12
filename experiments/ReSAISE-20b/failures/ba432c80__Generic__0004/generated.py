import requests
from urllib.parse import urlparse, parse_qs
import hmac

# Global dictionary mapping document URLs (or IDs) to their expected signatures.
# Example: DOC_SIGS = {"https://example.com/doc1.pdf": "abcd1234..."}
DOC_SIGS: dict[str, str] = {}

def _normalize_url(url: str) -> str:
    """
    Normalise the URL to a form that matches the keys in DOC_SIGS.
    For simplicity, we use the full URL without query parameters or fragments.
    """
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a document located at `url`.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    sign_hash : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at the provided URL is inaccessible (network error,
        non‑200 status code, etc.).
    """
    # Attempt to access the document to ensure it is reachable.
    try:
        resp = requests.head(url, timeout=5)
        resp.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Unable to access document at {url}") from exc

    # Normalise the URL so it can be looked up in DOC_SIGS.
    norm_url = _normalize_url(url)

    # Retrieve the expected signature; if not present, treat as invalid.
    expected = DOC_SIGS.get(norm_url)
    if expected is None:
        return False

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected, sign_hash)