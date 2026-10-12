import html

# XML template containing a placeholder for user supplied text.
xml_pattern = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_text}</message>
</response>"""

def create_xml_reply(user_text: str) -> str:
    """
    Return an XML string where the user's text is safely inserted into
    a predefined template.

    Parameters:
        user_text (str): The text supplied by the user that will be
                         inserted into the XML.

    Returns:
        str: The final XML string with user content safely escaped.
    """
    # Escape special XML characters to prevent injection (CWE‑74).
    safe_text = html.escape(user_text, quote=True)
    return xml_pattern.format(user_text=safe_text)

# Example usage:
if __name__ == "__main__":
    sample = "<script>alert('xss')</script>"
    print(create_xml_reply(sample))