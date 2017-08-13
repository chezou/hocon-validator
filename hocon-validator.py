from pyhocon import ConfigFactory
from pyhocon.exceptions import ConfigException
import yaml
from argparse import ArgumentParser

class color:
    OK = '\033[92m'
    WARN = '\033[93m'
    NG = '\033[91m'
    END_CODE = '\033[0m'

def print_ok(message):
    print(color.OK + message + color.END_CODE)

def print_ng(message):
    print(color.NG + message + color.END_CODE)

def validation(schema, conf, all_pass=True):
    if 'required' in schema:
        for e in schema['required']:
            if not e in schema['properties'].keys():
                print_ng('{} does not exist'.format(e))

    for e, current_schema in schema['properties'].items():
        _type = current_schema['type']
        if _type == 'object':
            try:
                child_conf = conf.get_config(e)
            except ConfigException:
                print_ng('{} does not exist or is not a object value.'.format(e))
                all_pass = False

            if 'required' in current_schema:
                all_pass = validation(current_schema, child_conf, all_pass)

        elif _type == 'string':
            try:
                conf.get_string(e)
            except ConfigException:
                print_ng('{} does not exist or is not a string value.'.format(e))
                all_pass = False

        elif _type == 'bool':
            try:
                conf.get_boolean(e)
            except ConfigException:
                print_ng('{} does not exist or is not a boolean value.'.format(e))
                all_pass = False

        elif _type == 'list':
            try:
                conf.get_list(e)
            except ConfigException:
                print_ng('{} does not exist or is not a list value.'.format(e))
                all_pass = False

        elif _type == 'float':
            try:
                conf.get_float(e)
            except ConfigException:
                print_ng('{} does not exist or is not a float value.'.format(e))
                all_pass = False

        else:
            print_ng("Invalid type: {}".format(_type))

    return all_pass

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("hocon_file", help="HOCON file for validation")
    parser.add_argument("schema_file", help="Schema file for HOCON")
    args = parser.parse_args()

    schema_file = args.schema_file
    hocon_file = args.hocon_file


    conf = ConfigFactory.parse_file(hocon_file)

    with open(schema_file, 'r') as f:
        schema = yaml.load(f)

    print("HOCON file: {}".format(hocon_file))
    print("Schema file: {}\n".format(schema_file))
    print("Start validation...")
    if validation(schema, conf):
        print_ok("All fields are valid!")
