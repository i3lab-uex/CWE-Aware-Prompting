import xml.sax.saxutils

# Predefined XML template with a placeholder for user input.
xml_design = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{input_data}</content>
</response>"""

def process_xml_reply(input_data: str) -> str:
    """
    Safely embed user-supplied content into an XML template.

    Args:
        input_data: The raw string submitted by the user.

    Returns:
        A well‑formed XML string with the input safely escaped.
    """
    # Escape special XML characters to prevent injection
    safe_input = xml.sax.saxutils.escape(input_data, entities={"'": "&apos;", '"': "&quot;"})
    return xml_design.format(input_data=safe_input)