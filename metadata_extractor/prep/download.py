from bs4 import BeautifulSoup
from datetime import datetime
from os.path import dirname, isfile, realpath                                                                                                                           
from re import search, sub
from requests import get, post
from xml.etree import ElementTree

start = datetime.now()

PATH_TO_DIRECTORY_OF_THIS_FILE = dirname(realpath(__file__))  


# for arcgis online
def get_urls_for_services(url_to_services):
    j = get(url_to_services + "?f=json").json()
    return [(service['name'], url_to_services + "/" + service['name'] + "/" + service['type']) for service in j['services']]

for service_name, url_to_service in get_urls_for_services("https://server.arcgisonline.com/arcgis/rest/services"):
    text = get(url_to_service).text
    path_to_file = PATH_TO_DIRECTORY_OF_THIS_FILE + "/metadata/ESRI/" + service_name
    if not isfile(path_to_file):
        with open(path_to_file, "wb") as f:
            f.write(text.encode("utf-8"))

# for geonodes
outputschemas = {
    "Atom": "http%3A%2F%2Fwww.w3.org%2F2005%2FAtom",
    "DIF": "http%3A%2F%2Fgcmd.gsfc.nasa.gov%2FAboutus%2Fxml%2Fdif%2F",
    "Dublin_Core": "http%3A%2F%2Fwww.opengis.net%2Fcat%2Fcsw%2F2.0.2",
    "ebRIM": "urn%3Aoasis%3Anames%3Atc%3Aebxml-regrep%3Axsd%3Arim%3A3.0",
    "FGDC": "http%3A%2F%2Fwww.opengis.net%2Fcat%2Fcsw%2Fcsdgm",
    "ISO": "http%3A%2F%2Fwww.isotc211.org%2F2005%2Fgmd"
}


with open(PATH_TO_DIRECTORY_OF_THIS_FILE + "/sources.txt") as f:
    list_of_sources = f.read().strip().split("\n")

for url_to_source in list_of_sources:

    print "url_to_source:", url_to_source

    # skip over commented
    if url_to_source.startswith("#"):
        print "skipped:", url_to_source
        continue

    try:
        url_to_capabilities = url_to_source.strip("/") + "/geoserver/wms?request=GetCapabilities&service=WMS&version=1.0.0"
        print "getting " + url_to_capabilities
        xml = get(url_to_capabilities).text

        with open("/tmp/tmpxml.xml", "wb") as f:
            f.write(xml.encode("utf-8"))

        tree = ElementTree.parse("/tmp/tmpxml.xml")

        print "tree:", type(tree)
        for onlineResource in tree.findall(".//MetadataURL/OnlineResource"):
            for key in onlineResource.keys():
                if "href" in key:
                    url = onlineResource.get(key)
                    if url:
                        layerId = search("(?<=id=)[^&]+", url).group(0)
                        for metatype in outputschemas:
                            metastring = outputschemas[metatype]
                            url_to_metadata_xml_file = sub("(?<=outputschema=)[^&]+", metastring, url)
                            path_to_file = PATH_TO_DIRECTORY_OF_THIS_FILE + "/metadata/" + metatype + "/" + layerId
                            if not isfile(path_to_file):
                                with open(path_to_file, "wb") as f:
                                    print "\tgetting", url_to_metadata_xml_file
                                    f.write(get(url_to_metadata_xml_file).text.encode("utf-8"))

        print "took", (datetime.now() - start).total_seconds(), "seconds"

    except Exception as e:
        print e
        raise e


