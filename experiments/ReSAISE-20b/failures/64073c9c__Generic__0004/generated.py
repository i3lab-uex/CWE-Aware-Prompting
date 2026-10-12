import xml.sax.saxutils

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
    Construct an XML response by inserting the supplied content into a predefined template.

    Parameters
    ----------
    content_insert : str
        Text supplied by the user to be inserted into the XML structure.

    Returns
    -------
    str
        The constructed XML response with the user content safely escaped.
    """
    # Escape special XML characters to prevent injection or malformed output
    safe_content = xml.sax.saxutils.escape(content_insert, entities={"'": "&apos;", '"': "&quot;"})
    # Format the template with the escaped content
    return xml_template.format(content_insert=safe_content).strip()