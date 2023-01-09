import re
import argparse
import warnings

def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'

def identifyAltText(image_markdown, line_number):
    # Check if the image markdown has alt text
    if "]" in image_markdown[2:]:
        alt_text = image_markdown[
            image_markdown.index("[") + 1 : image_markdown.index("]")
        ]
    else:
        alt_text = ""

    # Output the image markdown and the line number it appears on if it has alt text or "image" as the alt text
    if not alt_text or alt_text.lower() in ["image", "picture", "photo", "screen shot", "screenshot", "dialog", "interface"]:
        warnings.formatwarning = custom_formatwarning
        warnings.warn(str(f"\033[38;2;255;191;0m ⚠️ Line {line_number}: {image_markdown} has no useful alt text \033[0m"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="The path to the file")
    args = parser.parse_args()
    # Read the markdown file into a string
    with open(args.file_path, "r") as file:
        markdown_string = file.read()

    # Find all image markdown in the string
    image_markdown_pattern = r"!\[.*?\]\(.*?\)"
    image_markdown_matches = re.finditer(image_markdown_pattern, markdown_string)

    # Iterate through the image markdown matches
    for i, match in enumerate(image_markdown_matches):
        # Get the image markdown and the line number it appears on
        image_markdown = match.group()
        line_number = markdown_string[: match.start()].count("\n") + 1
        
        identifyAltText(image_markdown, line_number)

if __name__ == '__main__':
    main()
