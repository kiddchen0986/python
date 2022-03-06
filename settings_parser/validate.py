import sys
import os

from pysettings.loader import Loader
from pysettings.schema import Schema
from pysettings.config import Config

def main(argv):
    loader = Loader(os.path.abspath(os.path.dirname(argv[0])))
    config = loader.load_config("config.json")
    schema = loader.load_schema(config.get_schema_path())

    if len(argv) == 1:
        print("No input manifests, exiting")
        sys.exit(-1)

    for arg in argv[1:]:
        manifest = loader.load_manifest(arg)
        for file_name in manifest.get_sources()[0].get_file_list():
            result, error = schema.validate_json_file(file_name)
            if result:
                print(file_name + " validated successfully")
            else:
                print(file_name + " failed to validate: " + error)
                print("\nERROR\n")
                sys.exit(1)
    print("\nOK\n")
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
