from textnode import TextNode, TextType
from helpers import split_nodes_delimiter, split_nodes_link, markdown_to_blocks

def main():
    #dummy = TextNode("`code block` and then what", TextType.TEXT, "testurl.com")
    #dummy2 = TextNode("This is text with `more code`.", TextType.TEXT)
    #print(dummy)

    #print(f"Splitting {dummy} and {dummy2} into nodes")
    #new_nodes = split_nodes_delimiter([dummy], "`", TextType.CODE)
    #print("New nodes after splitting:")
    #print(new_nodes)

    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

    

if __name__ == "__main__":
    main()