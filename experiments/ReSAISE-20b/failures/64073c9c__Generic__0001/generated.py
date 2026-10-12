import xml.sax.saxutils

def generate_xml_message(content_insert: str) -> str:
    """
    Construct an XML message by inserting the supplied content into a predefined
    template. The function safely escapes any characters that have special meaning
    in XML to prevent injection or malformed documents.

    Parameters:
        content_insert (str): The user supplied text that will be inserted into
                              the XML structure.

    Returns:
        str: The fully formed XML string with the content inserted.
    """
    # Predefined template with a placeholder for user content
    xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<message>
    <content>{content_insert}</content>
</message>"""

    # Escape special XML characters in the user supplied content
    safe_content = xml.sax.saxutils.escape(content_insert)

    # Format the template with the escaped content
    return xml_template.format(content_insert=safe_content)