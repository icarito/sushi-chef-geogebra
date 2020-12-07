#!/usr/bin/env python

"""
Geogebra Chef that uses the IMSCP library to create and upload a channel
from the SCORM zip file downloaded from dropdown GeoGebra Project 
http://procomun.educalab.es/es/ode/view/1465806119010

Based on imscp library example.
Adapted by Sebastian Silva <sebastian@fuentelibre.org>
"""

import logging
import os
import sys
import tempfile
import getopt
import sh

from ricecooker.chefs import SushiChef
from ricecooker.classes import licenses

from imscp.core import extract_from_zip
from imscp.ricecooker_utils import make_topic_tree_with_entrypoints

script_dir = os.path.dirname(os.path.abspath(__file__))
TITLE = input("\nIngrese el título: ")
DESCRIPTION = input("\nIngrese la descripción: ")
FILE=input("\nRuta del archivo SCORM: ")
if os.path.isfile(FILE):
    MD5SUM = str(sh.md5sum(FILE))[:32]
    sh.ln("-s", FILE, MD5SUM+".zip")
    TMPFILE = MD5SUM+".zip"
else:
    sys.exit(0)

print ("Procesando: " + TITLE)
print ("            " + "="*len(TITLE))
print ("            " + DESCRIPTION + "\n")

class GeogebraChef(SushiChef):
    """
    The chef class that takes care of uploading channel to the content curation server.

    We'll call its `main()` method from the command line script.
    """
    channel_info = {
        'CHANNEL_SOURCE_DOMAIN': "geogebra.org",
        'CHANNEL_SOURCE_ID': "Recursos Geogebra",
        'CHANNEL_TITLE': TITLE,
        'CHANNEL_DESCRIPTION': DESCRIPTION,
        'CHANNEL_LANGUAGE': "es",
    }

    def construct_channel(self, **kwargs):
        """
        Create ChannelNode and build topic tree.
        """
        # create channel
        channel = self.get_channel()

        license = licenses.CC_BY_SALicense(copyright_holder="CeDeC")
        logging.basicConfig(level=logging.INFO)

        with tempfile.TemporaryDirectory() as extract_path:
            imscp_dict = extract_from_zip(os.path.join(script_dir, TMPFILE), license,
                    extract_path)
            for topic_dict in imscp_dict['organizations']:
                topic_tree = make_topic_tree_with_entrypoints(license,
                        os.path.join(script_dir, TMPFILE),
                        topic_dict, extract_path, tempfile.gettempdir())
                print('Adding topic tree to channel:', topic_tree)
                channel.add_child(topic_tree)

        return channel


if __name__ == '__main__':
    """
    This code will run when the sushi chef is called from the command line.
    """
    chef = GeogebraChef()
    chef.main()
    if os.path.isfile(TMPFILE):
        os.unlink(TMPFILE)
