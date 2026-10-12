import hashlib
import urllib.request
from typing import Dict

# Example of a pre‑defined dictionary that maps document URLs to their expected SHA‑256 signatures.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # "https://example.com/document.pdf": "5d41402abc4b2a76b9719d911017c592",
    # Add entries here
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remote document by comparing its SHA‑256 hash
    to the provided cryptographic signature.

    Parameters
    ----------
    location : str
        URL of the document to be verified.
    sign : str
        Expected cryptographic signature (hex string) for the document.

    Returns
    -------
    bool
        True if the computed signature matches the expected one, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the specified URL.
    """
    try:
        with urllib.request.urlopen(location, timeout=10) as response:
            data = response.read()
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Unable to retrieve document from {location}") from exc

    # Compute SHA‑256 hash of the retrieved data
    computed_hash = hashlib.sha256(data).hexdigest()

    # Verify against both the provided sign and the pre‑defined signature
    expected_sign = DOCUMENT_SIGNATURES.get(location)
    if expected_sign is not None:
        return computed_hash == sign and computed_hash == expected_sign

    # If no pre‑defined signature is stored, fall back to the supplied sign only
    return computed_hash == sign