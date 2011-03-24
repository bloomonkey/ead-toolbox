<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xsl:stylesheet []>

<!-- 
	This file was produced, and released as part of Cheshire for Archives v3.x.
	Copyright &#169; 2005-2008 the University of Liverpool, all rights reserved.
-->
	
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
  xmlns:dc="http://purl.org/dc/elements/1.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd"
  version="1.0">
  
	<xsl:output method="xml"/>
  
	<!-- Strip all audience=internal -->
	<xsl:template match='//*[@audience="internal"]' priority="100"/>

	<xsl:template match="/">
		<xsl:apply-templates/>
	</xsl:template>
  
	<xsl:template match="/ead">
		<oai_dc:dc>
		    <!-- always insert identifier -->
		    <dc:identifier>
				<xsl:call-template name="strip_space_and_lowercase">
					<xsl:with-param name="text">
						<xsl:value-of select="eadheader/eadid"/>
					</xsl:with-param>
				</xsl:call-template>
		     </dc:identifier>
		     <xsl:apply-templates select="archdesc/did"/>
		     <xsl:apply-templates select="archdesc/controlaccess/subject"/>
		     <xsl:apply-templates select="archdesc/scopecontent"/>
		     <xsl:apply-templates select="archdesc/langmaterial"/>
		</oai_dc:dc>
	</xsl:template>

	<xsl:template match="/c3component">
		<oai_dc:dc>
			<!-- always insert identifier -->
		    <dc:identifier>
				<xsl:call-template name="strip_space_and_lowercase">
					<xsl:with-param name="text">
						<xsl:value-of select="./*/did/unitid"/>
					</xsl:with-param>
				</xsl:call-template>
			</dc:identifier>
			<xsl:apply-templates select="./*/did"/>
		    <xsl:apply-templates select="./*/controlaccess/subject"/>
			<xsl:apply-templates select="./*/scopecontent"/>
			<xsl:apply-templates select="./*/langmaterial"/>
		</oai_dc:dc>
	</xsl:template>

  	<xsl:template match="did">
		<dc:title>
			<xsl:choose>
				<xsl:when test="./unittitle">
					<xsl:apply-templates select="./unittitle[1]"/>
				</xsl:when>
				<xsl:when test="/ead/archdesc/did/unittitle">
					<xsl:apply-templates select="/ead/archdesc/did/unittitle"/>
				</xsl:when>
				<xsl:when test="/ead/eadheader/filedesc/titlestmt/titleproper">
					<xsl:apply-templates select="/ead/eadheader/filedesc/titlestmt/titleproper"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:text>(untitled)</xsl:text>
				</xsl:otherwise>
			</xsl:choose>
		</dc:title>
		<xsl:apply-templates select="./did/origination"/>
  	</xsl:template>

	<!-- strip head tags - they're meaningless in Dublin Core -->
	<xsl:template match="head"/>
	
	<xsl:template match="origination">
		<dc:creator><xsl:apply-templates/></dc:creator>
	</xsl:template>

	<xsl:template match="subject">
		<dc:subject><xsl:apply-templates/></dc:subject>
	</xsl:template>
  
	<xsl:template match="scopecontent">
		<dc:description>
			<xsl:apply-templates/>
		</dc:description>
	</xsl:template>
  
	<xsl:template match="langmaterial">
	  	<xsl:for-each select="language">
			<dc:language>
				<xsl:value-of select="."/>
			</dc:language>
	  	</xsl:for-each>
	</xsl:template>
  
	<xsl:template name="strip_space_and_lowercase">
		<xsl:param name="uc" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>
		<xsl:param name="lc" select="'abcdefghijklmnopqrstuvwxyz'"/>
		<xsl:param name="text">
			<xsl:value-of select="."/>
		</xsl:param>
		<xsl:value-of select="translate(translate($text, ' ', ''), $uc, $lc)"/>
	</xsl:template>
 
	<xsl:template match="*">
		<xsl:text> </xsl:text>
		<xsl:apply-templates/>
	</xsl:template>

</xsl:stylesheet>
