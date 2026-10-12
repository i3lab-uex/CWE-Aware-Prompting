import xml.sax.saxutils

# Example XML template containing a placeholder `{input_data}`
xml_design = """
<response>
    <status>ok</status>
    <data>{input_data}</data>
</response>
"""

def process_xml_reply(input_data: str) -> str:
    """
    Insert user supplied content into an XML template safely.

    Parameters
    ----------
    input_data : str
        The raw user content that will be embedded into the XML.

    Returns
    -------
    str
        The final XML string with the user content inserted in place of the placeholder.

    Notes
    -----
    The function uses :func:`xml.sax.saxutils.escape` to neutralize special XML
    characters (`<`, `>`, `&`, `'`, and `"`) in the user input.  This mitigates
    CWE‑74 (Improper Neutralization of Special Elements in Output Used by a Downstream Component)
    by ensuring that the inserted data cannot break out of its intended element
    or inject additional XML markup.
    """
    # Escape any special XML characters in the user input
    safe_input = xml.sax.saxutils.escape(input_data, entities={"'": "&apos;", '"': "&quot;"})

    # Replace the placeholder with the escaped content
    return xml_design.format(input_data=safe_input)