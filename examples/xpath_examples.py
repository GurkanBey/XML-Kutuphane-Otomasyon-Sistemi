import xml.etree.ElementTree as ET
from lxml import etree
import os

def main():
    """
    Example of using XPath to query XML data
    """
    print("XPath Examples")
    print("==============")
    
    # Load the XML file
    xml_path = os.path.join(os.path.dirname(__file__), 'books.xml')
    tree = etree.parse(xml_path)
    root = tree.getroot()
    
    # Example 1: Get all book titles
    print("\nExample 1: Get all book titles")
    print("-----------------------------")
    titles = root.xpath('//book/title/text()')
    for title in titles:
        print(f"- {title}")
    
    # Example 2: Get books published after 1950
    print("\nExample 2: Get books published after 1950")
    print("--------------------------------------")
    recent_books = root.xpath('//book[year>1950]')
    for book in recent_books:
        title = book.xpath('./title/text()')[0]
        year = book.xpath('./year/text()')[0]
        print(f"- {title} ({year})")
    
    # Example 3: Get books in the Fantasy category
    print("\nExample 3: Get books in the Fantasy category")
    print("------------------------------------------")
    fantasy_books = root.xpath('//book[category="Fantasy"]')
    for book in fantasy_books:
        title = book.xpath('./title/text()')[0]
        author = book.xpath('./author/text()')[0]
        print(f"- {title} by {author}")
    
    # Example 4: Get book with id=3
    print("\nExample 4: Get book with id=3")
    print("---------------------------")
    book = root.xpath('//book[@id=3]')[0]
    title = book.xpath('./title/text()')[0]
    author = book.xpath('./author/text()')[0]
    year = book.xpath('./year/text()')[0]
    print(f"Title: {title}")
    print(f"Author: {author}")
    print(f"Year: {year}")
    
    # Example 5: Count number of books per category
    print("\nExample 5: Count number of books per category")
    print("------------------------------------------")
    categories = root.xpath('//book/category/text()')
    category_count = {}
    for category in categories:
        if category in category_count:
            category_count[category] += 1
        else:
            category_count[category] = 1
    
    for category, count in category_count.items():
        print(f"{category}: {count} book(s)")
    
    # Example 6: Get authors of books published before 1950
    print("\nExample 6: Get authors of books published before 1950")
    print("--------------------------------------------------")
    old_book_authors = root.xpath('//book[year<1950]/author/text()')
    for author in old_book_authors:
        print(f"- {author}")
    
    # Example 7: Find books with descriptions containing specific text
    print("\nExample 7: Find books with descriptions containing 'novel'")
    print("--------------------------------------------------------")
    novel_books = root.xpath('//book[contains(description, "novel")]')
    for book in novel_books:
        title = book.xpath('./title/text()')[0]
        print(f"- {title}")


if __name__ == "__main__":
    main()
