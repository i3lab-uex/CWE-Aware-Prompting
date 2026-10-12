import xml.sax.saxutils

def generate_xml_response(user_content: str) -> str:
    """
    Generate an XML response by embedding the provided user content into a template.

    Parameters
    ----------
    user_content : str
        The user-provided content to be embedded into the XML response.

    Returns
    -------
    str
        The generated XML response incorporating the escaped user content.
    """
    # Escape special characters to avoid malformed XML or injection
    safe_content = xml.sax.saxutils.escape(user_content, entities={"'": "&apos;", '"': "&quot;"})

    xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{user_content}</content>
</response>"""

    return xml_template.format(user_content=safe_content)