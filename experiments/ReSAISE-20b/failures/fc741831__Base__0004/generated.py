import requests
from urllib.parse import urlparse
import hmac

# Example dictionary of known signatures for remote documents.
# The keys are URLs and the values are expected cryptographic signature strings
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a1b2c3d4e5f678901234567890abcdef",
    # Add more entries as needed
}


def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate the integrity of a remote document by comparing its signature
    against a pre‑defined authoritative value.

    Parameters
    ----------
    url : str
        The URL of the document to retrieve and validate.
    crypt_signature : str
        The signature supplied for verification.

    Returns
    -------
    bool
        True if the supplied signature matches the stored signature for the URL,
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be fetched from the given URL.
    """
    # Ensure we have a valid absolute URL
    parsed = urlparse(url)
    if not (parsed.scheme and parsed.netloc):
        raise IOError(f"Invalid URL: {url}")

    # Retrieve the document content
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Failed to retrieve document from {url}") from exc

    # The content itself is not needed for signature comparison in this
    # simplified scenario, but we could compute a hash here if desired.
    _ = response.content  # placeholder to avoid unused variable warning

    # Retrieve the known signature for this URL
    expected_signature = DOCUMENT_SIGNATURES.get(url)
    if expected_signature is None:
        # If we have no record of the document, consider it invalid
        return False

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(crypt_signature, expected_signature)