import os
from lxml import etree


def main():
    """
    Example of using XSLT to transform XML data to HTML
    """
    # Load the XML file
    xml_path = os.path.join(os.path.dirname(__file__), 'books.xml')
    xml_tree = etree.parse(xml_path)
    
    # Create XSLT transformer
    xslt_content = '''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes"/>
    
    <xsl:template match="/">
        <html>
            <head>
                <title>Library Book Catalog</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        background-color: #f5f5f5;
                    }
                    h1 {
                        color: #333;
                        border-bottom: 2px solid #444;
                        padding-bottom: 10px;
                    }
                    .book {
                        background-color: white;
                        border: 1px solid #ddd;
                        padding: 15px;
                        margin-bottom: 15px;
                        border-radius: 5px;
                        box-shadow: 0 2px 3px rgba(0,0,0,0.1);
                    }
                    .book-title {
                        color: #2c3e50;
                        font-size: 20px;
                        margin-top: 0;
                    }
                    .book-author {
                        color: #7f8c8d;
                        font-style: italic;
                    }
                    .book-meta {
                        color: #7f8c8d;
                        font-size: 14px;
                        margin-bottom: 10px;
                    }
                    .book-description {
                        line-height: 1.5;
                    }
                    .category {
                        background-color: #3498db;
                        color: white;
                        padding: 3px 7px;
                        border-radius: 3px;
                        font-size: 12px;
                        display: inline-block;
                    }
                </style>
            </head>
            <body>
                <h1>Library Book Catalog</h1>
                <div class="catalog">
                    <xsl:apply-templates select="library/books/book"/>
                </div>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="book">
        <div class="book">
            <h2 class="book-title"><xsl:value-of select="title"/></h2>
            <p class="book-author">by <xsl:value-of select="author"/></p>
            <p class="book-meta">
                Published: <xsl:value-of select="year"/> | 
                ISBN: <xsl:value-of select="isbn"/> | 
                Publisher: <xsl:value-of select="publisher"/>
            </p>
            <span class="category"><xsl:value-of select="category"/></span>
            <p class="book-description">
                <xsl:value-of select="description"/>
            </p>
        </div>
    </xsl:template>
</xsl:stylesheet>
'''
    
    # Parse the XSLT content
    xslt_tree = etree.ElementTree(etree.fromstring(xslt_content))
    
    # Create transformer
    transform = etree.XSLT(xslt_tree)
    
    # Apply the transformation
    html_result = transform(xml_tree)
    
    # Save the result to an HTML file
    html_output_path = os.path.join(os.path.dirname(__file__), 'books_catalog.html')
    with open(html_output_path, 'wb') as f:
        f.write(etree.tostring(html_result, pretty_print=True))
        
    print(f"XSLT transformation complete. HTML output saved to {html_output_path}")
    print("Open this file in a web browser to view the formatted book catalog.")


if __name__ == "__main__":
    main()
