import requests

# Example dictionary of known document signatures (hash values, base64, etc.)
DOCUMENT_SIGNATURES = {
    # "https://example.com/doc1.pdf": "sha256:abcd1234...",
    # "https://example.com/report.txt": "sha256:efgh5678..."
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate that a remote document's cryptographic signature matches the expected value.

    Parameters
    ----------
    location : str
        URL of the remote document to validate.
    sign : str
        Cryptographic signature supplied for validation.

    Returns
    -------
    bool
        True if the provided signature matches the expected value for the document.
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    try:
        # Attempt to download the file; we only need a successful request
        response = requests.get(location, timeout=10)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as exc:
        # Any failure to fetch the document results in an IOError
        raise IOError(f"Unable to retrieve document from {location}") from exc

    # Retrieve the expected signature for this location, if any
    expected_sign = DOCUMENT_SIGNATURES.get(location)

    # If we have an expected signature, compare it to the supplied one
    if expected_sign is not None:
        return sign == expected_sign

    # If no signature is stored for this URL, treat it as invalid
    return False