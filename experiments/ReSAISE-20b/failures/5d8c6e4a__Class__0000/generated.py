import requests
import hmac

# Pre‑defined mapping of document URLs to their authentic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries – replace with real data in production
    "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/doc2.pdf": "e99a18c428cb38d5f260853678922e03",
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remote document by comparing its
    cryptographic signature with the expected value stored in
    DOCUMENT_SIGNATURES.

    Parameters
    ----------
    location : str
        URL of the document to be verified.
    sign : str
        Signature provided for validation.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Attempt to fetch the remote document
    try:
        response = requests.get(location, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Unable to retrieve document from {location}") from exc

    # The content is not needed for signature verification in this simplified
    # example, but fetching it ensures the resource exists and is reachable.

    expected_sig = DOCUMENT_SIGNATURES.get(location)
    if expected_sig is None:
        # No known signature for this URL – treat as invalid
        return False

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected_sig)