import xml.sax.saxutils

# Template for the XML response. The placeholder {user_content} will be replaced
# with properly escaped user-provided content.
xml_template = """
<response>
    <content>{user_content}</content>
</response>
"""

def generate_xml_response(user_content: str) -> str:
    """
    Generate an XML response by embedding the provided user content into a
    template. The user content is escaped to prevent XML injection or malformed
    documents.

    Args:
        user_content (str): The content supplied by the user.

    Returns:
        str: A well‑formed XML string containing the escaped content.
    """
    # Escape special XML characters to avoid breaking the structure
    safe_content = xml.sax.saxutils.escape(user_content, entities={
        '"': "&quot;", "'": "&apos;"
    })
    return xml_template.format(user_content=safe_content)