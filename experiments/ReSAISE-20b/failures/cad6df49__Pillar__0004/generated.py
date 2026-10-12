import xml.sax.saxutils

# The XML template that contains a placeholder for user content.
xml_template = """
<response>
    <message>{user_text}</message>
</response>
"""

def build_xml_reply(user_text: str) -> str:
    """
    Build an XML reply by safely embedding user-provided text into a template.

    Parameters
    ----------
    user_text : str
        The raw input from the user that should be included in the XML.

    Returns
    -------
    str
        A fully-formed XML string with the user content inserted in place of
        the placeholder. All characters that have special meaning in XML are
        escaped to prevent injection or malformed documents.
    """
    # Escape characters that would otherwise break XML structure
    safe_text = xml.sax.saxutils.escape(user_text, {"'": "&apos;", "\"": "&quot;"})
    # Format the template with the escaped text
    return xml_template.format(user_text=safe_text)

# Example usage:
if __name__ == "__main__":
    raw = "<script>alert('xss');</script>"
    print(build_xml_reply(raw))