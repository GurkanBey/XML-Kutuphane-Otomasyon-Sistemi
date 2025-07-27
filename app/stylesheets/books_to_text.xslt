<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text"/>
    
    <xsl:template match="/">
LIBRARY BOOK CATALOG
====================

Total Books: <xsl:value-of select="count(//book)"/>

<xsl:for-each select="//book">
<xsl:sort select="title"/>
TITLE: <xsl:value-of select="title"/>
AUTHOR: <xsl:value-of select="author"/>
YEAR: <xsl:value-of select="year"/>
ISBN: <xsl:value-of select="isbn"/>
PUBLISHER: <xsl:value-of select="publisher"/>
CATEGORY: <xsl:value-of select="category"/>
DESCRIPTION:
<xsl:value-of select="description"/>

--------------------------------------------------
</xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
