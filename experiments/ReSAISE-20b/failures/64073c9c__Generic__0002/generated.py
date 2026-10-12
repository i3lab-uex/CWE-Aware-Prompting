import xml.sax.saxutils

# Example XML template containing a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<message>
    <content>{content_insert}</content>
</message>"""

def generate_xml_message(content_insert: str) -> str:
    """
    Construct an XML message by inserting the supplied user content into
    a predefined template. The content is escaped to prevent malformed XML.

    Args:
        content_insert: Text supplied by the user that should be embedded
                        within the <content> element of the XML.

    Returns:
        A string containing the fully formed XML document.
    """
    # Escape special XML characters to avoid breaking the structure
    safe_content = xml.sax.saxutils.escape(content_insert)

    # Substitute the placeholder in the template
    return xml_template.format(content_insert=safe_content)