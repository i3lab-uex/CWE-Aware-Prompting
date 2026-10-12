import hashlib
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Example dictionary mapping document URLs to their expected SHA‑256 signatures.
DOCUMENT_SIGNATURES = {
    # "https://example.com/doc1.pdf": "e3b0c442... (hex digest)",
    # Add real entries here.
}

def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate a remotely hosted document against its expected cryptographic signature.

    Parameters
    ----------
    document_location : str
        URL of the document to retrieve and verify.
    crypto_sign : str
        Cryptographic signature (hex digest) provided for validation.

    Returns
    -------
    bool
        True if the retrieved document matches the expected signature; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from ``document_location``.
    """
    try:
        # Use a user‑agent header to avoid being blocked by some servers.
        req = Request(document_location, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=10) as response:
            content = response.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Could not retrieve document from {document_location}") from exc

    # Compute SHA‑256 hash of the downloaded content.
    sha256_hash = hashlib.sha256(content).hexdigest()

    # Compare against the provided signature.
    if crypto_sign.lower() != sha256_hash:
        return False

    # Additionally, verify against the pre‑defined dictionary if present.
    expected = DOCUMENT_SIGNATURES.get(document_location)
    if expected is not None and crypto_sign.lower() != expected.lower():
        return False

    return True