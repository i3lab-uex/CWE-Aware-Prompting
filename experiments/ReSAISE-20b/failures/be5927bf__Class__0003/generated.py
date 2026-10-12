import re
import html

def render_html_template(html_template: str, input_map: dict) -> str:
    """
    Render an HTML template by substituting placeholders with user-provided values.

    Args:
        html_template (str): The HTML template containing placeholders of the form {placeholder}.
        input_map (dict): Mapping from placeholder names to their replacement values.

    Returns:
        str: The rendered HTML with all placeholders replaced by escaped user input.

    Raises:
        ValueError: If a placeholder is missing from the input_map or if template processing fails.
    """

    # Regular expression to find placeholders of the form {name}
    placeholder_pattern = re.compile(r'\{(\w+)\}')

    # Function used for replacement; it escapes the user-provided value
    def replace_match(match: re.Match) -> str:
        key = match.group(1)
        if key not in input_map:
            raise ValueError(f"Missing value for placeholder: {key}")
        # Escape the user-provided input to avoid HTML injection
        return html.escape(str(input_map[key]), quote=True)

    try:
        rendered = placeholder_pattern.sub(replace_match, html_template)
    except Exception as exc:
        # Wrap any unexpected error in a ValueError for consistency
        raise ValueError(f"Template rendering failed: {exc}") from exc

    return rendered