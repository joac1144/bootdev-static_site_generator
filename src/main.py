import os
import shutil

from blocks import extract_title
from blocks import markdown_to_html_node

def main():
    copy_files("static", "public")

    generate_pages_recursive("content", "template.html", "public")


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    content_elements = os.listdir(dir_path_content)
    print(f"dir_path_content: \"{dir_path_content}\", elements: ", content_elements)
    for element in content_elements:
        element_path = os.path.join(dir_path_content, element)
        print(f"Looking at \"{element_path}\"")
        if os.path.isfile(element_path) and element.endswith(".md"):
            file_name = element.split(".")[0]
            dest_file_path = os.path.join(dest_dir_path, file_name + ".html")
            generate_page(element_path, template_path, dest_file_path)
        if os.path.isdir(element_path):
            dest_element_path = os.path.join(dest_dir_path, element)
            os.makedirs(dest_element_path)
            generate_pages_recursive(element_path, template_path, dest_element_path)


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise Exception("from_path does not exist")
    file = open(from_path)
    md = file.read()
    file.close()
    file = open(template_path)
    template = file.read()
    file.close()

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    page_content = template.replace("{{ Title }}", title)
    page_content = page_content.replace("{{ Content }}", html)

    with open(dest_path, "w") as file:
        file.write(page_content)


def copy_files(src_dir: str, dest_dir: str):
    # Make sure both src_dir and dest_dir exist
    if not os.path.exists(src_dir):
        raise Exception("src_dir does not exist")
    if not os.path.exists(dest_dir):
        raise Exception("dest_dir does not exist")

    src_dir_elements = os.listdir(src_dir)
    print(f"src directory: \"{src_dir}\", elements: {src_dir_elements}")

    # Delete all content from destination directory
    dest_dir_elements = os.listdir(dest_dir)
    print(f"dest directory: \"{dest_dir}\", elements: {dest_dir_elements}")
    delete_content(dest_dir)

    # Copy everything from src to dest
    copy_elements(src_dir, dest_dir)


def copy_elements(src: str, dest: str):
    elements = os.listdir(src)
    for element in elements:
        element_path = os.path.join(src, element)
        print(f"Copying element \"{element_path}\" to \"{dest}\"")
        if os.path.isfile(element_path):
            new_dest = shutil.copy(element_path, dest)
            print(f"Copied \"{element_path}\" to \"{new_dest}\"")
        if os.path.isdir(element_path):
            new_dest_path = os.path.join(dest, element)
            os.mkdir(new_dest_path)
            copy_elements(element_path, new_dest_path)


def delete_content(dir: str):
    dir_elements = os.listdir(dir)
    for element in dir_elements:
        path = os.path.join(dir, element)
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(f"File: {path}, reason: {e})")


if __name__ == "__main__":
    main()