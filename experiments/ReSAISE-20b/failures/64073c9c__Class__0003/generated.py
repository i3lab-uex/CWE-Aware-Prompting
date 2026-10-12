import xml.sax.saxutils

# Pre‑defined XML template with a placeholder for user content.
XML_TEMPLATE = """
<message>
    <header>
        <timestamp>{timestamp}</timestamp>
        <type>notification</type>
    </header>
    <body>
        {content_insert}
    </body>
</message>
"""

def generate_xml_message(content_insert: str) -> str:
    """
    Construct an XML message by inserting the provided content into a
    pre‑defined template. The user supplied content is escaped to avoid
    XML injection (CWE‑74).

    Parameters:
        content_insert (str): Text supplied by the user to be inserted into
                              the XML body.

    Returns:
        str: The complete XML message with escaped user content.
    """
    # Escape special XML characters in the user input
    safe_content = xml.sax.saxutils.escape(content_insert)

    # Populate the template; you can add more dynamic fields as needed
    xml_message = XML_TEMPLATE.format(
        timestamp=xml.sax.saxutils.escape(str(__import__('datetime').datetime.utcnow())),
        content_insert=safe_content
    )
    return xml_message.strip()