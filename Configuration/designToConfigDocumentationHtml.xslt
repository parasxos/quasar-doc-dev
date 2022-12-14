<xsl:transform version="2.0" xmlns:xml="http://www.w3.org/XML/1998/namespace" 
xmlns:xs="http://www.w3.org/2001/XMLSchema" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
xmlns:d="http://cern.ch/quasar/Design"
xmlns:fnc="http://cern.ch/quasar/Functions"
xsi:schemaLocation="http://www.w3.org/1999/XSL/Transform schema-for-xslt20.xsd ">
    <xsl:output indent="yes" method="xml"/>
    
    <xsl:function name="fnc:boundRestrictionTypeToSymbol">
    <xsl:param name="restrictionType"/>
    <xsl:choose>
    <xsl:when test="$restrictionType='minExclusive'">&gt;</xsl:when>
    <xsl:when test="$restrictionType='minInclusive'">&gt;=</xsl:when>
    <xsl:when test="$restrictionType='maxInclusive'">&lt;=</xsl:when>
    <xsl:when test="$restrictionType='maxExclusive'">&lt;</xsl:when>
    <xsl:otherwise><xsl:message terminate="yes">Type unsupported: <xsl:value-of select="$restrictionType"/></xsl:message></xsl:otherwise>
    </xsl:choose>
    </xsl:function>
    
    <xsl:template match="/">
    
    <html>
    
    <h1>Configuration documentation for <xsl:value-of select="/d:design/@projectShortName"/></h1>
    
    
    Jump to:
    <xsl:for-each select="/d:design/d:class">
    <a href="#class_{@name}"><xsl:value-of select="@name"/></a><xsl:text> </xsl:text>
    </xsl:for-each>
    
    <xsl:for-each select="/d:design/d:class">
    <xsl:sort select="@name"/>
    <a id="class_{@name}"><h2><xsl:value-of select="@name"/></h2></a>
    <xsl:if test="d:documentation">
        <div style="background-color:#eeeeff"><font color="blue">DOC</font><xsl:text> </xsl:text>
            <xsl:copy-of select="d:documentation"/>
        </div>
        <br/>
    </xsl:if>
    
    <xsl:choose>
        <xsl:when test="d:configentry | d:cachevariable[@initializeWith='configuration']">
        Configuration attributes (all mandatory):
        <ul>
        <xsl:for-each select="d:configentry | d:cachevariable[@initializeWith='configuration']">
            <li>
                <b><xsl:value-of select="@name"/></b> (<xsl:value-of select="@dataType"/>)
                <xsl:if test="d:documentation">
                    <div style="background-color:#eeeeff"><font color="blue">DOC</font><xsl:text> </xsl:text>
                    <xsl:copy-of select="d:documentation"/>
                    </div>
                </xsl:if>
                <xsl:if test="d:configRestriction">
                    <div style="background-color: #ffefef"><font color="red">Value restrictions</font>
                    <xsl:if test="d:configRestriction/d:restrictionByPattern"><br/>Pattern: <code><xsl:value-of select="d:configRestriction/d:restrictionByPattern/@pattern"/></code></xsl:if>
                    <xsl:if test="d:configRestriction/d:restrictionByEnumeration">
                        <br/>
                        Enumeration: 
                        <xsl:for-each select="d:configRestriction/d:restrictionByEnumeration/d:enumerationValue">
                            <code><xsl:value-of select="@value"/></code><xsl:if test="position() &lt; count(../d:enumerationValue)">|</xsl:if>
                        </xsl:for-each>
                    </xsl:if>
                    <xsl:if test="d:configRestriction/d:restrictionByBounds">
                        <br/>
                        Bounds:
                        <xsl:variable name="fieldName"><xsl:value-of select="@name"/></xsl:variable>
                        <xsl:for-each select="d:configRestriction/d:restrictionByBounds/@*">
                            <xsl:sort select="name()" order="descending" />
                            <code>
                            <xsl:if test="position() > 1"> AND </xsl:if>
                            <xsl:value-of select="$fieldName"/>
                            <xsl:value-of select="fnc:boundRestrictionTypeToSymbol(name())"/>
                            <xsl:value-of select="."/>
                            </code>
                        </xsl:for-each>
                    </xsl:if>
                    </div>
                </xsl:if>
                <br/>
            </li>
        </xsl:for-each>
        </ul>
            
        </xsl:when>
        <xsl:otherwise>
        This class(XML element) has no configuration attributes.
        </xsl:otherwise>
        
    </xsl:choose>
    
    Possible children:
    <xsl:for-each select="d:hasobjects[@instantiateUsing='configuration']">
    <a href="#class_{@class}"><xsl:value-of select="@class"/></a>
    </xsl:for-each>
    
    </xsl:for-each>


    
    
    </html>
    
    
    </xsl:template>
    
    </xsl:transform>
    