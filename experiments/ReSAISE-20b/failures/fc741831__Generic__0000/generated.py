import requests

# Pre‑defined dictionary mapping URLs to their expected cryptographic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries – replace with real data in production
    "https://example.com/doc1.pdf": "a3f5c9e8d4b2...",
    "https://example.com/doc2.pdf": "7c9e1f3a6d0b...",
}

def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate the integrity of a remote document by verifying its cryptographic signature.

    Parameters
    ----------
    url : str
        The URL of the remote document.
    crypt_signature : str
        The cryptographic signature claimed for this document.

    Returns
    -------
    bool
        True if the document can be retrieved and the signature matches the expected one;
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be fetched from the given URL.
    """
    # Attempt to download the document
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Could not retrieve document from {url}") from exc

    # Retrieve the expected signature for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(url)

    # If no entry exists, treat as invalid
    if expected_sig is None:
        return False

    # Compare the provided signature with the stored one
    return crypt_signature == expected_sig