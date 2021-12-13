# Copyright (c) 2018-2021 Fingerprint Cards AB <tech@fingerprints.com>
#
# All rights are reserved.
# Proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Any use is subject to an appropriate license granted by Fingerprint Cards AB.

import os
import sys
import datetime
import io

from pysettings.loader import Loader
from pysettings.settings import Settings
from pysettings.product import Product
from tools.testdata.gradient_checkerboard import GradientCheckerboard
from tools.testdata.swinging_checkerboard import SwingingCheckerboard
from tools.testdata.image_constant import ImageConstant
from tools.testdata.image_drive import ImageDrive
from tools.testdata.capacitance import Capacitance
from tools.testdata.test_vectors import TestVectors
from tools.testdata.module_quality2 import ModuleQuality2
from tools.testdata.module_quality import ModuleQuality
from tools.testdata.afd_cal import AfdCal
from tools.testdata.current_consumption import CurrentConsumption

import tools.common as Common

autogen_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'autogen')

def update_file(file_name, new_lines):
    with io.open(file_name, "w", newline='\n') as F:
        F.writelines(new_lines)


def get_hwid_list(product_config):
    hwid_list = []
    for entry in product_config:
        if entry["key"] == "sensor_hardware_id":
            hwid_list.append(entry["value"].lower())
    return hwid_list


def process_and_update(settings):
    test_vector = TestVectors()

    test_and_vector_data = {
        "gradientCheckerboard": GradientCheckerboard(),
        "swingingCheckerboard": SwingingCheckerboard(),
        "imageConstant": ImageConstant(),
        "imageDrive": ImageDrive(),
        "capacitance": Capacitance(),
        "test_vector": test_vector,
        "moduleQuality2": ModuleQuality2(),
        "moduleQuality": ModuleQuality(),
        "afdCal": AfdCal(),
        "currentConsumption": CurrentConsumption()
    }

    for product in settings.get_products():
        prod_name = product.get_product_name().upper().replace("?","")

        print('Processing %s' % prod_name)

        product_string = "PRODUCT_TYPE%s" % prod_name[:prod_name.rfind("_")].replace("FPC","")
        if product_string.endswith("TSMC") or product_string.endswith("SMIC"):
            product_string = product_string[:product_string.rfind("_")]

        test_vector.add_entry(product_string, product, prod_name)

        test_limits = product.get_limits()
        for test_name in test_limits.get_test_names():
            if test_name not in test_and_vector_data:
                print('No support for test: "%s", skipping it' % test_name)
                continue

            test_and_vector_data[test_name].add_entry(product_string, product.get_hwid_list(), test_limits.get_limits_test_data(test_name))


    print("Creating limits and vector files")

    for test_data in test_and_vector_data.values():
        update_file(test_data.get_full_filepath(),
            test_data.process())


def main(argv):
    loader = Loader('.')
    config = loader.load_config("config.json")
    manifest = loader.load_manifest("tools/manifest_testdata.json")
    settings = loader.load_settings(manifest.get_sources()[0], config)

    process_and_update(settings)
    print ("Done")

if __name__ == "__main__":
    if not os.path.exists(autogen_dir):
        os.makedirs(autogen_dir)
    # Set path of this file to working dir
    os.chdir(os.path.dirname(__file__))
    main(sys.argv)
