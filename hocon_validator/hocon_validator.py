from pyhocon import ConfigFactory
from pyhocon.tool import HOCONConverter
from pyhocon.exceptions import ConfigException
import yaml
import json
from argparse import ArgumentParser
from jsonschema.validators import Draft4Validator
from sys import stderr

class color:
    OK = '\033[92m'
    WARN = '\033[93m'
    NG = '\033[91m'
    END_CODE = '\033[0m'

def print_ok(message):
    print(color.OK + message + color.END_CODE)

def print_ng(message):
    print(color.NG + message + color.END_CODE)

class Validator:
    def __init__(self, schema):
        self.validator = Draft4Validator(schema)

    def validate(self, conf):
        conf_json = json.loads(HOCONConverter.to_json(conf), strict=False)
        errored = False
        for error in self.validator.iter_errors(conf_json):
            stderr.write("{}{}: {}{}".format(
                color.NG, error.instance, error.message, color.END_CODE))
            errored = True

        return not errored


def main():
    parser = ArgumentParser()
    parser.add_argument("hocon_file", help="HOCON file for validation")
    parser.add_argument("schema_file", help="Schema file of YAML format")
    args = parser.parse_args()

    schema_file = args.schema_file
    hocon_file = args.hocon_file

    conf = ConfigFactory.parse_file(hocon_file)

    with open(schema_file, 'r') as f:
        schema = yaml.load(f)

    print("HOCON file: {}".format(hocon_file))
    print("Schema file: {}\n".format(schema_file))
    print("Start validation...")

    validator = Validator(schema)

    if not validator.validate(conf):
        exit(-1)

if __name__ == '__main__':
    main()
