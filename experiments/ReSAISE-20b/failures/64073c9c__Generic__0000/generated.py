import xml.sax.saxutils as sax

# Predefined XML template with a placeholder for user content.
xml_template = """
<message>
    <header>
        <title>Response</title>
    </header>
    <body>
        {content_insert}
    </body>
</message>
"""

def generate_xml_message(content_insert: str) -> str:
    """
    Create an XML response by inserting user-supplied content into a predefined template.

    Parameters
    ----------
    content_insert : str
        Text supplied by the user to be inserted into the XML structure.

    Returns
    -------
    str
        The constructed XML response with the user content safely escaped.
    """
    # Escape special XML characters to prevent injection and malformed XML.
    safe_content = sax.escape(content_insert, entities={"'": "&apos;", '"': "&quot;"})
    return xml_template.format(content_insert=safe_content)