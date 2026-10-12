import xml.sax.saxutils

# Example XML template with a placeholder for user content.
xml_template = """
<response>
    <message>{user_text}</message>
</response>
"""

def build_xml_reply(user_text: str) -> str:
    """
    Safely embed user-provided text into a predefined XML template.

    Parameters
    ----------
    user_text : str
        The raw text supplied by the user that will be inserted into the XML.

    Returns
    -------
    str
        A complete XML string with the user content safely escaped.
    """
    # Escape special XML characters to prevent injection or malformed XML.
    safe_text = xml.sax.saxutils.escape(user_text, entities={'"': "&quot;", "'": "&apos;"})
    return xml_template.format(user_text=safe_text)

# Example usage
if __name__ == "__main__":
    user_input = '<script>alert("XSS")</script>'
    print(build_xml_reply(user_input))