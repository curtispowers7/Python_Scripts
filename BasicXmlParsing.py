import xml.etree.ElementTree as ET


XmlFile = '''<?xml version="1.0"?>
<data>
    <country name="Liechtenstein" comment="fuck you">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
'''

root = ET.fromstring(XmlFile)

Results = {}

for child in root:
    CountryName = child.attrib['name']
    Rank = child.find('rank').text
    Year = child.find('year').text
    Neighbors = child.findall('neighbor')
    if len(Neighbors) > 1:
        neighbs = []
        for Neighbor in Neighbors:
            neighbs.append(Neighbor.attrib['name'])
        Neighbors = neighbs
    else:
        Neighbors = Neighbors[0].attrib['name']
    print('{0} has a rank of {1}, was founded in the year {2}, and has the following neighbor(s) {3}'.format(CountryName, Rank, Year, Neighbors))
	
