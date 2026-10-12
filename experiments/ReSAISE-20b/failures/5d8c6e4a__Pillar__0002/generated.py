import hashlib
import requests

# Example pre‑defined dictionary (in real code this would be provided elsewhere)
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd3",
    # ... other entries ...
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document by comparing its
    cryptographic signature with a trusted value.

    Parameters
    ----------
    location : str
        URL of the document to validate.
    sign : str
        Cryptographic signature (hex digest) supplied for verification.

    Returns
    -------
    bool
        True if the signature matches the trusted value, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    try:
        # Retrieve the document; we only need the content to compute a hash
        response = requests.get(location, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        # Any network or HTTP error should be surfaced as an IOError
        raise IOError(f"Unable to retrieve document from {location}") from exc

    # Compute a SHA‑256 hash of the downloaded content
    computed_hash = hashlib.sha256(response.content).hexdigest()

    # Retrieve the expected signature from the trusted store
    expected_sign = DOCUMENT_SIGNATURES.get(location)

    # If there is no entry for this URL, we consider it unauthenticated
    if expected_sign is None:
        return False

    # Compare the computed hash to the supplied signature
    return computed_hash.lower() == sign.lower()