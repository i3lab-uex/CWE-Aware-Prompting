import xml.sax.saxutils as saxutils

# Predefined XML template containing a single placeholder `{user_text}`.
xml_pattern = """
<response>
    <message>{user_text}</message>
</response>
"""

def create_xml_reply(user_text: str) -> str:
    """
    Insert the supplied user text into a predefined XML template.

    Parameters
    ----------
    user_text : str
        The content submitted by the user. It will be inserted into the XML
        template at the position of `{user_text}`.

    Returns
    -------
    str
        The final XML string with the user content safely escaped.
    """
    # Escape characters that are special in XML to prevent injection
    safe_text = saxutils.escape(user_text, entities={"'": "&apos;", "\"": "&quot;"})
    # Format the template with the escaped text
    return xml_pattern.format(user_text=safe_text)