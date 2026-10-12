import os
import json
import hmac

# Global dictionary mapping a *trusted* signature to the file name that it is
# allowed to represent.  In a real system this would be populated from a secure
# source (e.g., a signed manifest or a hardware‑backed key store).
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (signature: filename)
    # "sha256-of-config1": "config1.json",
}

def handle_config_file(filename: str, sig: str):
    """
    Read a configuration file and return its contents as a dictionary if the
    provided cryptographic signature matches an entry in TRUSTED_CONFIG_SIGNATURES.
    
    Parameters:
        filename (str): Name of the configuration file to load.
        sig (str): Cryptographic signature supplied with the data.
    
    Returns:
        dict: Parsed configuration if the signature is valid.
        None: If the signature does not match or the file content cannot be parsed.
    
    Raises:
        IOError: If the requested configuration file does not exist or is unreadable.
    """
    # 1. Verify that the requested file exists
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' not found")

    # 2. Ensure the signature is trusted for this filename
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if expected_sig is None:
        # No trusted signature entry for this file
        return None

    # Use constant‑time comparison to avoid timing attacks (CWE‑693 concern)
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # 3. Read and parse the file contents
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:  # Catch file I/O or JSON errors
        raise IOError(f"Failed to read or parse configuration '{filename}': {exc}") from exc

    # 4. Return the parsed configuration
    return data