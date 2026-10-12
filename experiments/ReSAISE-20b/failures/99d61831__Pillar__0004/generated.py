import html

# Example template with a placeholder for user-provided content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <div id="content">{user_content}</div>
</body>
</html>
"""

def create_html_output(input_content: str) -> str:
    """
    Produce an HTML string by safely injecting user-provided content into a template.

    Parameters
    ----------
    input_content : str
        Dynamic content supplied by the user. This value is escaped to prevent XSS and
        other injection attacks before being inserted into the template.

    Returns
    -------
    str
        The final HTML string with the escaped user content inserted.
    """
    # Escape special characters to neutralize any malicious markup.
    safe_content = html.escape(input_content, quote=True)

    # Use a format string that guarantees the placeholder exists.
    try:
        final_html = html_template.format(user_content=safe_content)
    except KeyError as exc:
        # If the placeholder is missing, raise a clear error.
        raise ValueError("The HTML template does not contain the required placeholder "
                         "'{user_content}'.") from exc

    return final_html