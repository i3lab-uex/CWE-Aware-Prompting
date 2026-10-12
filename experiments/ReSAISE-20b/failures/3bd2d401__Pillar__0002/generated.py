import xml.sax.saxutils

# Predefined XML template with a placeholder for user content.
xml_design = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <data>{input_data}</data>
</response>"""

def process_xml_reply(input_data: str) -> str:
    """
    Insert the user supplied content into a predefined XML template.

    Parameters
    ----------
    input_data : str
        The raw content submitted by the user that will be embedded into the XML.

    Returns
    -------
    str
        The final XML string with user content safely escaped.
    """
    # Escape special XML characters to avoid malformed XML or injection
    safe_content = xml.sax.saxutils.escape(input_data, entities={"'": "&apos;", "\"": "&quot;"})
    # Format the template with the escaped content
    return xml_design.format(input_data=safe_content)