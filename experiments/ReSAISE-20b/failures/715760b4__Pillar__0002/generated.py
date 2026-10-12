import xml.sax.saxutils

# Predefined XML template with a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_entry}</message>
</response>"""

def produce_xml_message(user_entry: str) -> str:
    """
    Produce a fully‑formed XML message by inserting the supplied user_entry
    into a predefined template. The user content is escaped to prevent
    XML injection attacks and ensure well‑formedness.

    Args:
        user_entry: The string supplied by the user that should be embedded
                    in the XML response.

    Returns:
        A string containing the complete XML document with the user entry
        safely inserted.
    """
    # Escape characters that could break XML structure or allow injection.
    safe_entry = xml.sax.saxutils.escape(user_entry, {"'": "&apos;", "\"": "&quot;"})
    return xml_template.format(user_entry=safe_entry)