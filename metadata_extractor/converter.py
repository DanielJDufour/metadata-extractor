from re import search
from os.path import dirname, isfile, realpath
from string import Template
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, fromstring

PATH_TO_DIRECTORY_OF_THIS_FILE = dirname(realpath(__file__))

def save_metadata(metadata, _format="ISO 19115-2", path_to_dir="/tmp/"):
    print "starting save_metadata with", type(metadata), path_to_dir
    for d in metadata:
        #print "d:", d
        tree = ElementTree.parse(PATH_TO_DIRECTORY_OF_THIS_FILE + "/templates/ISO 19115-2.xml")
        #print "tree:", type(tree)
        #print "d:", d.keys()
        if "Bounding box" in d:

            polygon = tree.find('.//{http://www.isotc211.org/2005/gmd}extent//{http://www.isotc211.org/2005/gmd}polygon')

            boundingBox = d["Bounding box"]
            mg = search("(\d+) ?W", boundingBox)
            xmin = mg.group(1) if mg else None

            mg = search("(\d+) ?E", boundingBox)
            xmax = mg.group(1) if mg else None

            mg = search("(\d+) ?S", boundingBox)
            ymin = mg.group(1) if mg else None

            mg = search("(\d+) ?N", boundingBox)
            ymax = mg.group(1) if mg else None

            polygon.append(fromstring(Template("""<gml:Polygon srsName="urn:ogc:def:crs:EPSG::4326" gml:id="Polygon1" xmlns:gml="http://www.opengis.net/gml/3.2"><gml:exterior><gml:LinearRing><gml:posList srsDimension="2">$xmin $ymin $xmax $ymin $xmax $ymax $xmin $ymax $xmin $ymin</gml:posList></gml:LinearRing></gml:exterior></gml:Polygon>""").substitute(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)))

        abstract = d.get('Abstract', None) or d.get('Abstract (Description)', None) or d.get('Description', None) or d.get("Description (Abstract)", None)
        if abstract:
            tree.find(".//{http://www.isotc211.org/2005/gmd}abstract//{http://www.isotc211.org/2005/gco}CharacterString").text = abstract

        summary = d.get('Summary', None) or d.get('Summary (Purpose)', None) or d.get('Summary', None) or d.get("Purpose", None)
        if summary:
            tree.find(".//{http://www.isotc211.org/2005/gmd}purpose//{http://www.isotc211.org/2005/gco}CharacterString").text = summary

        supplementalInfo = []
        for key in ["Data type and format", "Units", "Valid range of data values", "Fill values", "Data type/precision"]:
            v = d.get(key, None)
            if v:
                supplementalInfo.append(key + ": " + v)
        if supplementalInfo:
            tree.find(".//{http://www.isotc211.org/2005/gmd}supplementalInformation//{http://www.isotc211.org/2005/gco}CharacterString").text = " | ".join(supplementalInfo)

        path_to_write = path_to_dir.rstrip("/") + "/" + d.get('NAME', "iso") + ".xml"
        #print "path:", path_to_write
        tree.write(path_to_write)
