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

def validate(schema, conf):
    all_pass = True
    if not 'properties' in schema:
        return all_pass

    for e, current_schema in schema['properties'].items():
        _type = current_schema['type']
        if _type == 'object':
            try:
                child_conf = conf.get_config(e)
            except ConfigException:
                if 'required' in schema and e in schema['required']:
                    print_ng('{} is required field'.format(e))
                print_ng('{} is not a object value.'.format(e))
                all_pass = False

            if 'required' in current_schema:
                all_pass = all_pass and validate(current_schema, child_conf)

        elif _type == 'string':
            try:
                conf.get_string(e)
            except ConfigException:
                if 'required' in schema and e in schema['required']:
                    print_ng('{} is required field'.format(e))
                print_ng('{} is not a string value.'.format(e))
                all_pass = False

        elif _type == 'bool':
            try:
                conf.get_bool(e)
            except ConfigException:
                if 'required' in schema and e in schema['required']:
                    print_ng('{} is required field'.format(e))
                print_ng('{} is not a boolean value.'.format(e))
                all_pass = False

        elif _type == 'list':
            try:
                child_confs = conf.get_list(e)
            except ConfigException:
                if 'required' in schema and e in schema['required']:
                    print_ng('{} is required field'.format(e))
                print_ng('{} is not a list value.'.format(e))
                all_pass = False

            for child_conf in child_confs:
                all_pass = all_pass and validate(current_schema, child_conf)

        elif _type == 'float':
            try:
                conf.get_float(e)
            except ConfigException:
                if 'required' in schema and e in schema['required']:
                    print_ng('{} is required field'.format(e))
                print_ng('{} is not a float value.'.format(e))
                all_pass = False

        else:
            print_ng("Invalid type: {}".format(_type))

    return all_pass

validation = validate


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
    if validate(schema, conf):
        print_ok("All fields are valid!")
    else:
        exit(-1)


if __name__ == '__main__':
    main()
