import xml.sax.saxutils as saxutils

def produce_xml_message(user_entry: str) -> str:
    """
    Produce a well‑formed XML message by inserting the user entry into
    a predefined template, escaping any characters that would break the XML.

    Args:
        user_entry (str): The content supplied by the user.

    Returns:
        str: A complete XML string with the user entry safely embedded.
    """
    # Define the template once; use a placeholder that format() can replace
    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?><response>'
        '<message>{user_entry}</message></response>'
    )

    # Escape special XML characters to avoid injection or malformed XML
    safe_entry = saxutils.escape(user_entry, entities={"'": "&apos;", '"': "&quot;"})

    # Return the formatted XML string
    return xml_template.format(user_entry=safe_entry)