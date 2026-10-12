import requests
import hmac

# Pre‑defined mapping of document URLs to their authentic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "sha256:abcd1234...",
    # "https://example.org/report.txt": "sha256:efgh5678..."
}

def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate the integrity of a remote document by checking its cryptographic signature.

    Parameters
    ----------
    url : str
        The URL of the document to be verified.
    crypt_signature : str
        The signature provided for verification.

    Returns
    -------
    bool
        True if the provided signature matches the authentic one, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Attempt to fetch the remote resource to ensure it is reachable
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        # Wrap any network/HTTP error into an IOError to match the requirement
        raise IOError(f"Unable to retrieve document from {url}") from exc

    # Retrieve the expected signature for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(url)

    if expected_sig is None:
        # If we have no record of the document, treat it as invalid
        return False

    # Use constant‑time comparison to mitigate timing attacks (CWE‑345)
    return hmac.compare_digest(expected_sig, crypt_signature)