import os
from pysettings.loader import Loader

from collections import OrderedDict
import pandas as pd

def process_and_update(settings):
    for product in settings.get_products():
        hw_id_list = product.get_hwid_list()
        for hw_id in hw_id_list:
            ordered_dict = OrderedDict()
            prod_name = product.get_product_name().lower()
            revision = product.get_revision()
            ordered_dict['product name'] = prod_name
            ordered_dict['hardware id'] = hw_id
            ordered_dict['rrs revision'] = revision
            yield ordered_dict


def main():
    loader = Loader('.')
    config = loader.load_config("config.json")
    manifest = loader.load_manifest("tools/manifest_rrs_supported.json")
    data_list = []
    for source in manifest.get_sources():
        print('Processing %s' % source.get_name())
        settings = loader.load_settings(source, config)
        data_list.extend(list(process_and_update(settings)))

    data_frame = pd.DataFrame(data_list)
    data_frame.to_excel('rrs_version.xls', encoding='utf-8')

    print("Done")

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
