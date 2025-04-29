from textnode import TextNode, TextType

def main():
    dummy = TextNode("This is a dummy", TextType.BOLD, "testurl.com")
    print(dummy)

if __name__ == "__main__":
    main()