import xml.sax.saxutils

def produce_xml_message(user_entry: str) -> str:
    """
    Safely embed user input into a predefined XML template.

    Args:
        user_entry (str): Input provided by the user that must be inserted
                          into the XML structure.

    Returns:
        str: A well‑formed XML response with the user content safely escaped.
    """
    xml_template = (
        "<response>\n"
        "  <data>{user_entry}</data>\n"
        "</response>"
    )

    # Escape special XML characters to prevent injection or malformed XML
    safe_entry = xml.sax.saxutils.escape(user_entry, entities={"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(user_entry=safe_entry)