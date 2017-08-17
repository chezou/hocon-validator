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

    _type = schema['type']
    if _type is None:
        if conf:
            print_ng('{} is not a null value'.format(conf))
            return False

    elif _type == 'string':
        if not isinstance(conf, str):
            print_ng('{} is not a string value'.format(conf))
            return False

    elif _type == 'integer':
        if not isinstance(conf, int):
            print_ng('{} is not a float value'.format(conf))
            return False

        if isinstance(conf, bool):
            print_ng('{} is not a float value'.format(conf))
            return False

    elif _type in ['float', 'number']:
        if not isinstance(conf, int) and not isinstance(conf, float):
            print_ng('{} is not a float value'.format(conf))
            return False

        if isinstance(conf, bool):
            print_ng('{} is not a float value'.format(conf))
            return False

    elif _type == 'object':
        if not isinstance(conf, dict):
            print_ng('{} is not a object value'.format(conf))
            return False

        if 'properties' in schema:
            for k, v in schema['properties'].items():
                try:
                    child_conf = conf.get(k)
                    all_pass = all_pass and validate(v, child_conf)
                except ConfigException:
                    if 'required' in schema and k in schema['required']:
                        print_ng('{} is a required field'.format(k))
                        all_pass = False

            return all_pass

    elif _type == 'bool':
        if not isinstance(conf, bool):
            print_ng('{} is not a boolean value'.format(conf))
            return False

    elif _type in ['list', 'array']:
        if 'items' in schema:
            __items = schema['items']
            if isinstance(__items, dict):
                for c in conf:
                    all_pass = all_pass and validate(__items, c)

            elif isinstance(__items, list):
                for dic, c in zip(__items, conf):
                    all_pass = all_pass and validate(dic, c)
            else:
                all_pass = False

        return all_pass

    else:
        print_ng("Invalid type: {}".format(_type))
        return False

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
