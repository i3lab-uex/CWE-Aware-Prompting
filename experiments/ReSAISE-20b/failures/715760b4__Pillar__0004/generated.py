import xml.sax.saxutils

# XML template with a placeholder for user-provided content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_entry}</message>
</response>"""

def produce_xml_message(user_entry: str) -> str:
    """
    Produce a well‑formed XML response by safely embedding the user entry.

    Args:
        user_entry (str): Raw input from the user that will be inserted into
                          the XML message. It may contain characters that need
                          to be escaped.

    Returns:
        str: A complete XML document with the user entry safely inserted.
    """
    # Escape characters that have special meaning in XML
    safe_entry = xml.sax.saxutils.escape(user_entry, entities={"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(user_entry=safe_entry)