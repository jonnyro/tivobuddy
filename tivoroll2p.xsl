<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:t="http://www.tivo.com/developer/calypso-protocol-1.6/"
                xmlns="http://www.w3.org/1999/xhtml"
                exclude-result-prefixes="t"
                version="1.0">

  <xsl:output omit-xml-declaration="yes"/>

  <xsl:template match="t:TiVoContainer">
    <div class="tivoroll">
      <p>
        <xsl:apply-templates/>
      </p>
    </div>
  </xsl:template>

<xsl:template match="t:Item/t:Details/t:Title"><xsl:value-of select="."/><br/></xsl:template>
<xsl:template match="t:Item/t:Details/t:EpisodeTitle"><xsl:value-of select="."/><br/></xsl:template>

<xsl:template match="t:Item/t:Details/t:Description"><xsl:value-of select="."/><br/></xsl:template>

<xsl:template match="t:Item/t:Links/t:Content/t:Url"><xsl:value-of select="."/><br/></xsl:template>

  <xsl:template match="text()"/>

</xsl:stylesheet>
