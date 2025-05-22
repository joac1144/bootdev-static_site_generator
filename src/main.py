import os
import shutil

def main():
    copy_files("static", "public")

def copy_files(src_dir: str, dest_dir: str):
    # Make sure both src_dir and dest_dir exist
    if not os.path.exists(src_dir):
        raise Exception("src_dir does not exist")
    if not os.path.exists(dest_dir):
        raise Exception("dest_dir does not exist")

    src_dir_elements = os.listdir(src_dir)
    print(f"src directory: \"{src_dir}\", elements: ", src_dir_elements)

    # Delete all content from destination directory
    dest_dir_elements = os.listdir(dest_dir)
    print(f"dest directory: \"{dest_dir}\", elements", dest_dir_elements)
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