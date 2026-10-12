import xml.sax.saxutils

# Predefined XML template containing a single placeholder {input_data}
xml_design = """
<response>
    <status>success</status>
    <data>{input_data}</data>
</response>
"""

def process_xml_reply(input_data: str) -> str:
    """
    Insert user-supplied content into a predefined XML template.

    Parameters
    ----------
    input_data : str
        The content supplied by the user to be inserted into the XML.

    Returns
    -------
    str
        The final XML string with `input_data` safely escaped and placed in the template.

    Notes
    -----
    * The function uses :func:`xml.sax.saxutils.escape` to neutralize characters that
      could otherwise break XML structure or introduce injection vulnerabilities.
    * If the template does not contain the placeholder ``{input_data}``, the
      function simply returns the original template unchanged.

    Example
    -------
    >>> process_xml_reply('<foo>bar</foo>')
    '<response>\\n    <status>success</status>\\n    <data>&lt;foo&gt;bar&lt;/foo&gt;</data>\\n</response>'
    """
    # Escape user input to prevent XML injection
    safe_input = xml.sax.saxutils.escape(input_data, {"'": "&apos;", '"': "&quot;"})

    # Replace the placeholder; if absent, return template unchanged
    if "{input_data}" in xml_design:
        return xml_design.replace("{input_data}", safe_input)
    return xml_design