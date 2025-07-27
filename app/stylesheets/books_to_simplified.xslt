<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="yes"/>
    
    <xsl:template match="/">
        <library-catalog>
            <metadata>
                <generated-at>
                    <xsl:value-of select="current-dateTime()"/>
                </generated-at>
                <book-count>
                    <xsl:value-of select="count(//book)"/>
                </book-count>
                <categories>
                    <xsl:for-each select="//category[not(. = preceding::category)]">
                        <xsl:sort select="."/>
                        <category>
                            <xsl:value-of select="."/>
                        </category>
                    </xsl:for-each>
                </categories>
            </metadata>
            
            <books>
                <xsl:for-each select="//book">
                    <xsl:sort select="year" order="descending"/>
                    <book id="{@id}">
                        <basic-info>
                            <title><xsl:value-of select="title"/></title>
                            <author><xsl:value-of select="author"/></author>
                            <year><xsl:value-of select="year"/></year>
                        </basic-info>
                        <publishing-info>
                            <isbn><xsl:value-of select="isbn"/></isbn>
                            <publisher><xsl:value-of select="publisher"/></publisher>
                        </publishing-info>
                        <classification>
                            <category><xsl:value-of select="category"/></category>
                        </classification>
                    </book>
                </xsl:for-each>
            </books>
        </library-catalog>
    </xsl:template>
</xsl:stylesheet>
