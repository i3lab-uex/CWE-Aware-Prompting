import xml.sax.saxutils

def build_xml_reply(user_text: str, xml_template: str) -> str:
    """
    Build an XML reply by inserting the user-provided text into a template.

    Args:
        user_text: Text supplied by the user to be inserted into the XML.
        xml_template: A string containing an XML template with a single
                      placeholder `{user_text}`.

    Returns:
        A string containing the fully-formed XML with the user text safely
        escaped to prevent injection or malformed XML.

    Notes:
        - The function uses `xml.sax.saxutils.escape` to convert special
          characters (&, <, >, ", ') into their corresponding XML entities.
        - Only one placeholder `{user_text}` is expected in the template. If
          multiple placeholders are present, only the first will be replaced.
    """
    # Escape special XML characters in user input
    escaped_text = xml.sax.saxutils.escape(user_text, {"'": "&apos;"})
    # Replace the placeholder in the template
    return xml_template.format(user_text=escaped_text)