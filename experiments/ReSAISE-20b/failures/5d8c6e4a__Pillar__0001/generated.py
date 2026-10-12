import hashlib
import urllib.request
from urllib.error import URLError, HTTPError

# Example dictionary of pre‑computed SHA-256 signatures for remote documents.
# In practice this would be populated from a trusted source.
DOCUMENT_SIGNATURES = {
    # "https://example.com/doc1.pdf": "a3f5c2... (hex string)",
    # "https://example.com/doc2.txt": "4b8e1d... (hex string)",
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document.

    Parameters
    ----------
    location : str
        URL pointing to the document that needs verification.
    sign : str
        The expected cryptographic signature (hex string).

    Returns
    -------
    bool
        True if the computed signature matches the expected one,
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Ensure we are dealing with a string signature
    if not isinstance(sign, str):
        raise ValueError("Signature must be a hex string")

    try:
        # Use a short timeout and verify TLS certificates
        with urllib.request.urlopen(location, timeout=10) as resp:
            content = resp.read()
    except (URLError, HTTPError) as exc:
        # Wrap network errors into IOError to match specification
        raise IOError(f"Unable to retrieve document from {location}") from exc

    # Compute SHA-256 hash of the retrieved content
    computed_hash = hashlib.sha256(content).hexdigest()

    # Retrieve the expected signature from the trusted dictionary
    expected_sig = DOCUMENT_SIGNATURES.get(location)

    # If there is no known signature for this URL, consider it invalid
    if expected_sig is None:
        return False

    # Compare computed hash with both the stored signature and the provided one
    if computed_hash != expected_sig:
        return False

    # The provided signature must also match the stored one
    if sign.lower() != expected_sig.lower():
        return False

    return True