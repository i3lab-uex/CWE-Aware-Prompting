import xml.sax.saxutils as saxutils

# Pre‑defined XML template containing a placeholder for user content.
xml_template = """
<response>
    <content>{input_content}</content>
</response>
"""

def create_xml_output(input_content: str) -> str:
    """
    Create an XML response by safely inserting user-supplied content into a
    predefined template.

    Parameters:
        input_content (str): Text supplied by the user to be inserted into
                             the XML structure.

    Returns:
        str: The constructed XML response with the user content escaped.
    """
    # Escape special XML characters to prevent injection attacks (CWE‑74).
    safe_content = saxutils.escape(input_content, entities={"'": "&apos;", '"': "&quot;"})
    return xml_template.format(input_content=safe_content)