import xml.sax.saxutils

# Predefined XML template with a placeholder for user content.
xml_template = """
<response>
    <message>{user_entry}</message>
</response>
"""

def produce_xml_message(user_entry: str) -> str:
    """
    Safely embed user-provided input into an XML template.

    Args:
        user_entry: The string supplied by the user to be inserted into
                    the XML structure.

    Returns:
        A well‑formed XML string with the user content safely escaped.
    """
    # Escape characters that are significant in XML to prevent injection
    safe_entry = xml.sax.saxutils.escape(user_entry, {"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(user_entry=safe_entry)