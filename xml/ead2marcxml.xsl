<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
				xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				xmlns:marc="http://www.loc.gov/MARC21/slim">
				
	<xsl:output method="xml"/>

	<xsl:template match="/">
		<!-- TODO: Auto-generated template -->
		<marc:record>
			<marc:leader></marc:leader>
			<xsl:apply-templates select="ead"/>
		</marc:record>
	</xsl:template>
	
	<xsl:template match="ead">
		<xsl:apply-templates select="archdesc/did"/>
		<xsl:apply-templates select="archdesc//arrangement[1]"/>
		<xsl:apply-templates select="archdesc//accessrestrict[1]"/>
		<xsl:apply-templates select="archdesc//scopecontent[1]"/>
		<xsl:apply-templates select="archdesc//bioghist[1]"/>
	</xsl:template>
	
	<xsl:template match="did">
		<xsl:apply-templates select="langmaterial"/>
		<xsl:apply-templates select="origination" mode="main"/>
		<xsl:apply-templates select="unittitle" mode="stmt"/>
		<xsl:apply-templates select="unitdate"/>
		<xsl:apply-templates select="physdesc"/>
	</xsl:template>
	
	<xsl:template match="langmaterial">
		<xsl:for-each select="language">
			<marc:datafield tag="041">
				<marc:subfield code="a">
					<xsl:value-of select="./@langcode"/>
				</marc:subfield>
			</marc:datafield>
		</xsl:for-each>
	</xsl:template>
	
	<xsl:template match="origination" mode="main">
		<xsl:choose>
			<xsl:when test="persname">
				<marc:datafield tag="100">
					<marc:subfield code="a">
						<xsl:value-of select="."/>
					</marc:subfield>
				</marc:datafield>
			</xsl:when>
			<xsl:when test="corpname">
				<marc:datafield tag="110">
					<marc:subfield code="a">
						<xsl:value-of select="."/>
					</marc:subfield>
				</marc:datafield>
			</xsl:when>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="unittitle" mode="main">
		<marc:datafield tag="130">
			<marc:subfield code="a">
				<xsl:value-of select="."/>
			</marc:subfield>
		</marc:datafield>
	</xsl:template>
	
	<xsl:template match="unittitle" mode="stmt">
		<marc:datafield tag="245">
			<marc:subfield code="a">
				<xsl:value-of select="./text()"/>
			</marc:subfield>
			<xsl:if test="unitdate[@type='inclusive']">
				<marc:subfield code="f">
					<xsl:value-of select="unitdate[@type='inclusive']"/>
				</marc:subfield>
			</xsl:if>
			<xsl:if test="unitdate[@type='bulk']">
				<marc:subfield code="g">
					<xsl:value-of select="unitdate[@type='bulk']"/>
				</marc:subfield>
			</xsl:if>
		</marc:datafield>
	</xsl:template>
	
	<xsl:template match="unitdate">
		<marc:datafield tag="260">
			<marc:subfield code="c">
				<xsl:value-of select="./text()"/>
			</marc:subfield>
		</marc:datafield>
	</xsl:template>
	
	<xsl:template match="physdesc">
		<marc:datafield tag="300">
			<marc:subfield code="a">
				<xsl:apply-templates/>
			</marc:subfield>
		</marc:datafield>
	</xsl:template>
	
	<xsl:template match="arrangement">
		<marc:datafield tag="351">
			<marc:subfield code="a">
				<xsl:apply-templates/>
			</marc:subfield>
			<xsl:if test="/ead/archdesc/@level">
				<marc:subfield code="c">
					<xsl:value-of select="/ead/archdesc/@level"/>
				</marc:subfield>
			</xsl:if>
		</marc:datafield>
	</xsl:template>
	
	<xsl:template match="accessrestrict">
		<marc:datafield tag="506">
			<marc:subfield code="a">
				<xsl:apply-templates/>
			</marc:subfield>
		</marc:datafield>
	</xsl:template>
	
	<xsl:template match="scopecontent">
		<marc:datafield tag="520">
			<marc:subfield code="a">
				<xsl:apply-templates/>
			</marc:subfield>
		</marc:datafield>
	</xsl:template>
	
	<xsl:template match="bioghist">
		<marc:datafield tag="545">
			<marc:subfield code="a">
				<xsl:apply-templates/>
			</marc:subfield>
		</marc:datafield>
	</xsl:template>
</xsl:stylesheet>