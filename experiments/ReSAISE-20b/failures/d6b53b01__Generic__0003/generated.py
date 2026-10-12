import hashlib
import urllib.request
from urllib.error import URLError, HTTPError

# Example pre‑defined dictionary of valid signatures for known documents.
DOCUMENT_SIGNATURES = {
    # "https://example.com/file.txt": "5d41402abc4b2a76b9719d911017c592",
    # Add actual URLs and their expected SHA‑256 hex digests here.
}

def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document.

    Parameters
    ----------
    document_location : str
        URL of the remote document.
    crypto_sign : str
        Expected cryptographic signature (hex digest).

    Returns
    -------
    bool
        True if the retrieved document matches the provided signature and
        the stored reference in DOCUMENT_SIGNATURES; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    try:
        with urllib.request.urlopen(document_location) as response:
            data = response.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to retrieve document from {document_location}") from exc

    # Compute SHA‑256 digest of the retrieved data
    sha256 = hashlib.sha256()
    sha256.update(data)
    computed_digest = sha256.hexdigest()

    # Compare against the provided signature
    if crypto_sign.lower() != computed_digest:
        return False

    # Verify against the known signature for this URL (if any)
    expected_digest = DOCUMENT_SIGNATURES.get(document_location)
    if expected_digest and crypto_sign.lower() != expected_digest.lower():
        return False

    return True