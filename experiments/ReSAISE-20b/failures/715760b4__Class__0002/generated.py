import xml.sax.saxutils as saxutils

# Predefined XML template with a placeholder for user content
xml_template = """
<response>
    <message>{user_entry}</message>
</response>
"""

def produce_xml_message(user_entry: str) -> str:
    """
    Safely embed the user-provided input into an XML template.

    Args:
        user_entry (str): The content supplied by the user.

    Returns:
        str: A fully-formed XML string with the user content safely escaped.
    """
    # Escape special XML characters to prevent injection
    safe_entry = saxutils.escape(user_entry, entities={"'": "&apos;", '"': "&quot;"})
    return xml_template.format(user_entry=safe_entry)