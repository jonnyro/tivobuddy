<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:t="http://www.tivo.com/developer/calypso-protocol-1.6/"
                xmlns="http://www.w3.org/1999/xhtml"
                exclude-result-prefixes="t"
                version="1.0">

  <xsl:output method="text" omit-xml-declaration="yes"/>

  <xsl:template match="t:TiVoContainer">
	<Episode>
        <xsl:apply-templates/>
	</Episode>
  </xsl:template>

<xsl:template match="t:Item/t:Details/t:Title">Show|<xsl:value-of select="."/><xsl:text>&#x0A;</xsl:text></xsl:template><xsl:template match="t:Item/t:Details/t:EpisodeTitle">EpisodeTitle|<xsl:value-of select="."/><xsl:text>&#x0A;</xsl:text></xsl:template><xsl:template match="t:Item/t:Details/t:Description">Description|<xsl:value-of select="."/><xsl:text>&#x0A;</xsl:text></xsl:template>
<xsl:template match="t:Item/t:Links/t:Content/t:Url">URL|<xsl:value-of select="."/><xsl:text>&#x0A;</xsl:text></xsl:template>
<xsl:template match="text()"/>
</xsl:stylesheet>
 
