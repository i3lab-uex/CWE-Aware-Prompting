import xml.sax.saxutils

# The XML template containing a placeholder for user content.
xml_template = """
<response>
    <message>{content_to_add}</message>
</response>
"""

def build_xml_response(content_to_add: str) -> str:
    """
    Construct an XML response by safely inserting user-supplied content into
    a predefined template.

    Parameters:
        content_to_add (str): The text supplied by the user that will be
                              inserted into the <message> element.

    Returns:
        str: The complete XML string with user content safely escaped.
    """
    # Escape special XML characters to prevent injection attacks
    safe_content = xml.sax.saxutils.escape(content_to_add, entities={"'": "&apos;", '"': "&quot;"})
    return xml_template.format(content_to_add=safe_content)