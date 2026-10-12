import xml.sax.saxutils

def build_xml_reply(user_text: str) -> str:
    """
    Safely embed user-provided text into an XML template.

    Args:
        user_text: The raw string supplied by the user that must be included
            inside an XML element.

    Returns:
        A string containing a complete XML document with the user text
        properly escaped to prevent XML injection (CWE‑74).

    Notes:
        - The function uses xml.sax.saxutils.escape to convert the characters
          &, <, >, ", and ' into their corresponding XML entities.
        - No additional validation is performed; callers should ensure the
          template itself is safe and that user_text meets any other
          application‑level constraints.
    """
    # Escape special XML characters in the user input
    safe_user_text = xml.sax.saxutils.escape(user_text, {"'": "&apos;"})

    # Define the XML template with a placeholder for user content
    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<response>\n'
        '    <message>{user_text}</message>\n'
        '</response>'
    )

    # Insert the escaped user text into the template
    return xml_template.format(user_text=safe_user_text)