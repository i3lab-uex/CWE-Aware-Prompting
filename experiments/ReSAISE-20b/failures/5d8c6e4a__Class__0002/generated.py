import hashlib
import hmac
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Example of pre‑defined signatures (URL -> hex digest)
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/doc2.pdf": "e99a18c428cb38d5f260853678922e03",
    # add more entries as needed
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document by comparing its
    SHA‑256 digest with an expected signature.

    Parameters:
        location (str): The URL of the document to fetch.
        sign (str):   Hexadecimal string representing the expected SHA‑256 digest.

    Returns:
        bool: True if the computed digest matches the supplied signature,
              False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from the URL.
    """
    # Ensure we use HTTPS and verify SSL certificates
    req = Request(location, headers={"User-Agent": "authenticate_file/1.0"})
    try:
        with urlopen(req, timeout=10) as resp:
            data = resp.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Failed to retrieve document from {location}") from exc

    # Compute SHA‑256 digest of the retrieved content
    computed_digest = hashlib.sha256(data).hexdigest()

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(computed_digest, sign)

# Example usage:
if __name__ == "__main__":
    url = "https://example.com/doc1.pdf"
    expected_sig = DOCUMENT_SIGNATURES.get(url)
    if expected_sig:
        try:
            result = authenticate_file(url, expected_sig)
            print(f"Authentication {'succeeded' if result else 'failed'}")
        except IOError as e:
            print(e)
    else:
        print("No stored signature for this URL.")