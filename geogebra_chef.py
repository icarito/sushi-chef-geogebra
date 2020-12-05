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

from ricecooker.chefs import SushiChef
from ricecooker.classes import licenses

from imscp.core import extract_from_zip
from imscp.ricecooker_utils import make_topic_tree_with_entrypoints

script_dir = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[1:]

class GeogebraChef(SushiChef):
    """
    The chef class that takes care of uploading channel to the content curation server.

    We'll call its `main()` method from the command line script.
    """
    channel_info = {
        'CHANNEL_SOURCE_DOMAIN': "geogebra.org",
        'CHANNEL_SOURCE_ID': "test geogebra SCORM upload",
        'CHANNEL_TITLE': "Test SCORM",
        'CHANNEL_DESCRIPTION': "Cilindro de pruebas",
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
            imscp_dict = extract_from_zip(os.path.join(script_dir, '2b49248a9f57d1541124639dbfee72a7.zip'), license,
                    extract_path)
            for topic_dict in imscp_dict['organizations']:
                topic_tree = make_topic_tree_with_entrypoints(license,
                        os.path.join(script_dir, '2b49248a9f57d1541124639dbfee72a7.zip'),
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
