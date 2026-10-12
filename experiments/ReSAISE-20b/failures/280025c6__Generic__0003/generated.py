import re

def inject_custom_header(header_content: str) -> str:
    """
    Insert a user-supplied value as a custom header in the HTTP response headers.
    
    The function sanitizes the input by removing any characters that are not
    printable ASCII (0x20-0x7E) and by stripping CR/LF characters that could
    break the header format. It also removes any colons to prevent injection
    of additional header fields.
    
    Parameters:
        header_content (str): The user-provided custom header value.
        
    Returns:
        str: A well-formed header string, e.g. "X-Custom-Header: <sanitized_value>".
    """
    # Remove CR, LF and any characters outside printable ASCII
    sanitized = re.sub(r'[^\x20-\x7E]', '', header_content)
    
    # Remove any remaining colons to avoid header injection
    sanitized = sanitized.replace(':', '')
    
    # Trim leading/trailing whitespace
    sanitized = sanitized.strip()
    
    return f"X-Custom-Header: {sanitized}"