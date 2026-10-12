import xml.sax.saxutils as saxutils

# Example XML template with a placeholder for user content.
xml_template = """
<response>
    <data>{content_to_add}</data>
</response>
"""

def build_xml_response(content_to_add: str) -> str:
    """
    Construct an XML response by inserting the user-provided content
    into a predefined XML template. The content is safely escaped to
    avoid malformed XML or injection issues.

    Args:
        content_to_add (str): Text supplied by the user to be inserted
            into the XML structure.

    Returns:
        str: The constructed XML response with the content embedded.
    """
    # Escape special XML characters to prevent injection or parsing errors
    safe_content = saxutils.escape(content_to_add, entities={"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(content_to_add=safe_content)