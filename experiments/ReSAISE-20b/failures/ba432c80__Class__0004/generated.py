import requests
import hmac
from urllib.parse import urlparse

# Global dictionary mapping document URLs to their expected signatures.
DOC_SIGS = {
    # Example entries (replace with real values in production)
    "https://example.com/docs/contract.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/docs/terms.txt": "1234567890abcdef",
}


def _normalize_url(url: str) -> str:
    """
    Normalise a URL so that different representations of the same resource
    map to an identical string. This is a simple implementation that strips
    fragments and sorts query parameters.
    """
    parsed = urlparse(url)
    # Reconstruct URL without fragment
    return (
        f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        + ("?" + "&".join(sorted(parsed.query.split("&"))) if parsed.query else "")
    )


def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    value for a document located at *url*.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    sign_hash : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        ``True`` if the signature matches the expected value, otherwise
        ``False``.

    Raises
    ------
    IOError
        If the document at *url* is inaccessible (network errors, non‑200 status,
        etc.). The function does not perform any content validation beyond
        the signature check, but it must confirm that the resource is reachable.
    """
    # Normalise URL to avoid mismatches caused by different representations
    norm_url = _normalize_url(url)

    # Check that we have a known signature for this URL
    expected_sig = DOC_SIGS.get(norm_url)
    if expected_sig is None:
        # Unknown document – treat as inaccessible to avoid revealing
        # information about internal mapping.
        raise IOError(f"Document '{url}' not found in trusted signature database")

    # Ensure the remote resource is reachable (minimal check, no content download)
    try:
        response = requests.head(norm_url, timeout=5)
        if not response.ok:
            raise IOError(f"Unable to access document: HTTP {response.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Failed to access document: {exc}") from exc

    # Use a timing‑attack resistant comparison
    return hmac.compare_digest(sign_hash, expected_sig)