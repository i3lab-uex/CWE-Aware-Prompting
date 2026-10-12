import hashlib
import hmac
from urllib.parse import urlparse, urlunparse

import requests


# Example signature store (URL -> expected hex‑encoded SHA256 hash)
DOCUMENT_SIGNATURES = {
    # "https://example.com/doc1.pdf": "3a7bd3e2360f5d9c...",
    # Add real entries here
}


def _normalize_url(url: str) -> str:
    """
    Normalise the URL for consistent dictionary lookup.
    Removes fragment and query parts, keeps scheme, netloc and path.
    """
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))


def _compute_signature(content: bytes) -> str:
    """
    Compute a SHA256 hash of the document content and return it as
    a hexadecimal string.  The same algorithm must be used to produce
    the stored signatures in `DOCUMENT_SIGNATURES`.
    """
    return hashlib.sha256(content).hexdigest()


def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate that a remote document's signature matches the known
    cryptographic signature.

    Parameters
    ----------
    url : str
        URL of the document to be verified.
    crypt_signature : str
        Hexadecimal representation of the signature supplied by the caller.

    Returns
    -------
    bool
        True if the provided signature matches the stored one, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved (e.g., network error or non‑200 status).
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Could not retrieve document from {url}") from exc

    # Compute the signature of the retrieved content
    computed_sig = _compute_signature(resp.content)

    # Normalise URL for lookup in the signature dictionary
    norm_url = _normalize_url(url)

    # Retrieve the expected signature, if any
    expected_sig = DOCUMENT_SIGNATURES.get(norm_url)

    # If no stored signature exists, we cannot validate
    if expected_sig is None:
        return False

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(computed_sig, expected_sig) and \
           hmac.compare_digest(crypt_signature.lower(), expected_sig)