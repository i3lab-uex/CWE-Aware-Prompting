import requests
from urllib.parse import urlparse, urlunparse

# Global dictionary mapping document URLs to their expected signatures
DOC_SIGS = {
    # Example entries – replace with real values
    "https://example.com/docs/report.pdf": "abcdef1234567890",
    "https://example.org/files/data.csv": "0123456789abcdef",
}


def _canonical_url(url: str) -> str:
    """
    Normalise a URL so that equivalent URLs map to the same string.
    This is important because DOC_SIGS keys may be canonicalised.
    """
    parsed = urlparse(url)
    # Ensure scheme and netloc are lower‑cased
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    # Remove default ports
    if (scheme == "http" and netloc.endswith(":80")) or (
        scheme == "https" and netloc.endswith(":443")
    ):
        netloc = netloc.rsplit(":", 1)[0]
    return urlunparse((scheme, netloc, parsed.path, "", "", ""))


def check_document(url: str, sign_hash: str) -> bool:
    """
    Validate that the cryptographic signature `sign_hash` matches the expected
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
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    IOError
        If the document at `url` cannot be accessed (e.g., network error,
        non‑200 HTTP status, or timeout).
    """
    # Normalise the URL to match keys in DOC_SIGS
    canon_url = _canonical_url(url)

    # Verify that we have a known signature for this URL
    expected_sig = DOC_SIGS.get(canon_url)
    if expected_sig is None:
        # No known signature – treat as invalid
        return False

    # Attempt to access the remote document to ensure it is reachable.
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Any network or HTTP error is treated as an IO problem
        raise IOError(f"Unable to access document at {url}") from exc

    # If we reach here, the document is accessible and we can compare signatures
    return sign_hash == expected_sig