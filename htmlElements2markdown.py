import argparse
import os
import re
from bs4 import BeautifulSoup


def alphabetize_html_attributes(html: str) -> str:
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all elements with attributes
    for element in soup.find_all(attrs=True):
        # Get the element's attributes as a dictionary
        attrs = element.attrs

        # Sort the attributes by key
        sorted_attrs = dict(sorted(attrs.items()))

        # Set the element's attributes to the sorted dictionary
        element.attrs = sorted_attrs

    # Return the modified HTML as a string
    return str(soup)


def convert_images_to_markdown(html: str) -> str:
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find all img elements
    for img in soup.find_all("img"):
        # Get the src attribute
        src = img["src"]

        # Replace the img element with a markdown image syntax
        img.replace_with(f"![image]({src})")

    # Return the modified HTML as a string
    return str(soup)


def read_markdown_file(file_path: str) -> str:
    try:
        with open(file_path, "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except:
        print(f"Error: There was a problem reading the file '{file_path}'.")


def convert_links_to_markdown(html: str) -> str:
    try:
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Find all link elements
        for a in soup.find_all("a"):
            # Get the href attribute and the text of the link
            href = a["href"]
            text = a.text

            # Replace the link element with a markdown link syntax
            a.replace_with(f"[{text}]({href})")

        # Return the modified HTML as a string
        return str(soup)
    except:
        print("Error: There was a problem parsing the HTML.")


# only convert <a> elements with relative URIs


def convert_relative_links_to_markdown(html: str) -> str:
    try:
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Find all link elements
        for a in soup.find_all("a"):
            # Get the href attribute and the text of the link
            href = a["href"]
            text = a.text

            # Check if the href is an absolute URL
            if not bool(re.match(r"^https?://", href)):
                # Replace the link element with a markdown link syntax
                a.replace_with(f"[{text}]({href})")

        # Return the modified HTML as a string
        return str(soup)
    except:
        print("Error: There was a problem parsing the HTML.")


def convert_relative_images_to_markdown(html: str) -> str:
    try:
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Find all img elements
        for img in soup.find_all("img"):
            # Get the src attribute
            src = img["src"]

            # Check if the src is a relative URI
            if not bool(re.match(r"^https?://", src)):
                # Replace the img element with a markdown image syntax
                img.replace_with(f"![image]({src})")

        # Return the modified HTML as a string
        return str(soup)
    except:
        print("Error: There was a problem parsing the HTML.")


def add_new_to_filename(file_path: str) -> str:
    # Split the file path into its components
    directory, file_name = os.path.split(file_path)
    name, extension = os.path.splitext(file_name)

    # Create the new file name
    new_file_name = f"{name}.new{extension}"

    # Join the directory and the new file name
    new_file_path = os.path.join(directory, new_file_name)

    return new_file_path


def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="The path to the file")
    args = parser.parse_args()
    output_file = add_new_to_filename(args.file_path)
    # Read the file
    html = read_markdown_file(args.file_path)
    html = alphabetize_html_attributes(html)
    while True:
        # Print the menu
        print("Menu:")
        print("1. Convert all <a> elements to markdown syntax")
        print(
            "2. Convert <a> elements with relative href attributes to markdown syntax"
        )
        print("3. Convert all <img> elements to markdown syntax")
        print(
            "4. Convert <img> elements with relative src attributes to markdown syntax"
        )
        print("5. Quit")

        # Get the user's choice
        choice = input("Enter your choice: ")

        # Convert the choice to an integer
        try:
            choice = int(choice)
        except ValueError:
            print("Error: Please enter a valid number")
            continue

        # Take action based on the choice
        if choice == 1:
            modified_html = convert_links_to_markdown(html)
            if modified_html is not None:
                content = modified_html
        elif choice == 2:
            modified_html = convert_relative_links_to_markdown(html)
            if modified_html is not None:
                content = modified_html
        elif choice == 3:
            modified_html = convert_images_to_markdown(html)
            if modified_html is not None:
                content = modified_html
        elif choice == 4:
            modified_html = convert_relative_images_to_markdown(html)
            if modified_html is not None:
                content = modified_html
        elif choice == 5:
            break
        else:
            print("Error: Please enter a valid number")
    with open(output_file, 'w') as f:
        f.write(content)


if __name__ == "__main__":
    main()
