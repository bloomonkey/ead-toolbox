<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns="http://www.w3.org/1999/xhtml"
	>

	<xsl:output method="xml"/>

	<xsl:template match="/">
		<xsl:apply-templates/>
	</xsl:template>
	
	<xsl:template match="ead">
		<table>
			<tbody>
				<tr>
					<td><xsl:text>3.1.1 Reference Code</xsl:text></td>
					<td>
						<xsl:choose>
							<xsl:when test="archdesc/did/unitid">
								<xsl:apply-templates select="archdesc/did/unitid"/>
							</xsl:when>
							<xsl:otherwise>
								<xsl:apply-templates select="eadheader/eadid"/>
							</xsl:otherwise>
						</xsl:choose>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.1.2 Title</xsl:text></td>
					<td>
						<xsl:choose>
							<xsl:when test="./archdesc/did/unittitle">
								<xsl:apply-templates select="./archdesc/did/unittitle"/>
							</xsl:when>
							<xsl:when test="./eadheader/filedesc/titlestmt/titleproper">
								<xsl:apply-templates select="./eadheader/filedesc/titlestmt/titleproper"/>
							</xsl:when>
							<xsl:otherwise>
								<xsl:text>(untitled)</xsl:text>
							</xsl:otherwise>
						</xsl:choose>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.1.3 Dates</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc/did/unitdate"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.1.4 Level of Description</xsl:text></td>
					<td>
						<xsl:value-of select="./archdesc/@level"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.1.5 Extent and medium of the unit</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//physdesc[1]"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.2.1 Name of Creator</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//origination[1]"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.2.2 Administrative / Biographical History</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//bioghist[1]"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.2.3 Archival History</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//custodhist[1]"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.2.4 Immediate Source of Acquisition</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//acqinfo[1]"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.3.1 Scope and Content</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//scopecontent[1]"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.3.2 Appraisal, Destruction and Scheduling</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//appraisal[1]"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.3.3 Accruals</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//accruals[1]"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.3.4 System of Arrangement</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//arrangement[1]"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.4.1 Conditions Governing Use</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//accessrestrict"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.4.2 Conditions Governing Reproduction</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//userestrict"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.4.3 Language / scripts of material</xsl:text></td>
					<td>
						<ul>
							<xsl:for-each select="./archdesc//langmaterial/language">
								<li>
									<xsl:apply-templates select="."/>
								</li>
							</xsl:for-each>
						</ul>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.4.4 Physical Characteristics and Technical Requirements</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//phystech[1]"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.4.5 Finding Aids</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//otherfindaid"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.5.1 Existence and Location of Originals</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//originalsloc"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.5.2 Existence and Location of Copies</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//altformavail"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.5.3 Related Units of Description</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//relatedmaterial"/>
						<xsl:apply-templates select="./archdesc//separatedmaterial"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.5.4 Publication Note</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//bibliography"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.6.1 Note</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//odd"/>
						<xsl:apply-templates select="./archdesc//note"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.7.1 Note</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//processinfo"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.7.2 Rules or Conventions</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//descrules"/>
					</td>
				</tr>
				<tr>
					<td><xsl:text>3.7.3 Date(s) of Descriptions</xsl:text></td>
					<td>
						<xsl:apply-templates select="./archdesc//processinfo//date"/>
					</td>
				</tr>
			</tbody>
		</table>
		
	</xsl:template>
	
</xsl:stylesheet>