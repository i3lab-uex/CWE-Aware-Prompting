import requests
from requests.exceptions import RequestException, HTTPError
import hmac

# Example global dictionary of document URLs to their expected signatures.
# In practice this should be populated from a secure source.
DOC_SIGS = {
    # 'https://example.com/doc1.pdf': 'expected_signature_hash',
}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that the cryptographic signature of a remote document matches
    the expected value stored in DOC_SIGS.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    sign_hash : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the provided signature matches the expected one,
        False otherwise.

    Raises
    ------
    IOError
        If the document at ``url`` is inaccessible (network error or non‑2xx status).
    """
    # Validate that we have a known signature for this URL
    expected = DOC_SIGS.get(url)
    if expected is None:
        # If we don't know the signature, treat it as invalid.
        return False

    try:
        # Attempt to fetch the document to ensure it's reachable.
        # A timeout prevents hanging on unresponsive servers.
        response = requests.get(url, timeout=10)
        # Raise an HTTPError if the status is not 2xx.
        response.raise_for_status()
    except (RequestException, HTTPError) as exc:
        # Wrap any network/HTTP errors in an IOError to match the spec.
        raise IOError(f"Unable to access document at {url}") from exc

    # Use constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(sign_hash, expected)