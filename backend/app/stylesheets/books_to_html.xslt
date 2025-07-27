<?xml version="1.0" encoding="UTF-8"?>
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
                        color: #555;
                        font-size: 14px;
                        margin: 5px 0;
                    }
                    .book-description {
                        margin-top: 10px;
                        font-size: 15px;
                        line-height: 1.4;
                    }
                    .summary {
                        background-color: #eaf2f8;
                        padding: 10px 15px;
                        border-radius: 4px;
                        margin-bottom: 20px;
                    }
                </style>
            </head>
            <body>
                <h1>Library Book Catalog</h1>
                
                <div class="summary">
                    <p>Total Books: <strong><xsl:value-of select="count(//book)"/></strong></p>
                </div>
                
                <xsl:for-each select="//book">
                    <xsl:sort select="title"/>
                    <div class="book">
                        <h2 class="book-title"><xsl:value-of select="title"/></h2>
                        <p class="book-author">by <xsl:value-of select="author"/></p>
                        <p class="book-meta">
                            <strong>Year:</strong> <xsl:value-of select="year"/> |
                            <strong>ISBN:</strong> <xsl:value-of select="isbn"/> |
                            <strong>Publisher:</strong> <xsl:value-of select="publisher"/>
                        </p>
                        <p class="book-meta"><strong>Category:</strong> <xsl:value-of select="category"/></p>
                        <div class="book-description">
                            <xsl:value-of select="description"/>
                        </div>
                    </div>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
