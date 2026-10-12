import hashlib
import requests

# Example pre‑defined dictionary of known signatures.
# In a real application this would be populated from a secure source.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a3f5c2b8e9d4... (hex signature)",
    "https://example.com/doc2.txt": "7b9e1d4c6f0a... (hex signature)",
    # Add more entries as required.
}

def _compute_sha256(data: bytes) -> str:
    """Return the SHA‑256 hex digest of the given data."""
    return hashlib.sha256(data).hexdigest()


def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remote document.

    Parameters
    ----------
    location : str
        The URL of the document to be verified.
    sign : str
        The cryptographic signature (hex digest) supplied for verification.

    Returns
    -------
    bool
        True if the signature matches the known value for this URL,
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    try:
        # Perform a GET request with a reasonable timeout and stream the content
        response = requests.get(location, timeout=10, stream=True)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Unable to retrieve document from {location}") from exc

    # Read the content in chunks to avoid loading huge files into memory.
    sha256 = hashlib.sha256()
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive chunks
            sha256.update(chunk)

    computed_signature = sha256.hexdigest()

    # Retrieve the expected signature for this URL from the dictionary.
    expected_signature = DOCUMENT_SIGNATURES.get(location)

    # If we don't have a stored signature, consider it invalid.
    if expected_signature is None:
        return False

    # Compare computed signature with the supplied one and the stored one.
    if computed_signature != sign:
        return False

    # Final check against known valid signatures
    return computed_signature == expected_signature