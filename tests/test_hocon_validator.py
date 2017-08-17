import unittest
import hocon_validator
from pyhocon import ConfigFactory
import yaml

class TestHoconValidator(unittest.TestCase):
    def test_validate(self):
        hocon = """
# This example is from https://github.com/chimpler/pyhocon/blob/master/README.md
{
  databases {
    # MySQL
    active = true
    enable_logging = false
    resolver = null
    # you can use substitution with unquoted strings. If it it not found in the document, it defaults to environment variables
    home_dir = ${HOME} # you can substitute with environment variables
    "mysql" = {
      host = "abc.com" # change it
      port = 3306 # default
      username: scott // can use : or =
      password = tiger, // can optionally use a comma
      // number of retries
      retries = 3
    }
  }
  // this will be appended to the databases dictionary above
  databases.ips = [
    192.168.0.1 // use white space or comma as separator
    "192.168.0.2" // optional quotes
    192.168.0.3, # can have a trailing , which is ok
  ]

}
"""

        schema_yaml = """
title: test-schema
type: object
required:
  - databases
properties:
  databases:
    type: object
    required:
      - active
      - enable_logging
      - home_dir
      - mysql
      - ips
    properties:
      active:
        type: bool
      enable_logging:
        type: bool
      resolver:
        type: null
      home_dir:
        type: string
      mysql:
        type: object
        required:
          - host
          - port
          - username
          - password
        properties:
          host:
            type: string
          port:
            type: float
          username:
            type: string
          password:
            type: string
          retries:
            type: float

      ips:
        type: list
"""
        conf = ConfigFactory.parse_string(hocon)
        schema = yaml.load(schema_yaml)
        self.assertTrue(hocon_validator.validate(schema, conf))

    def test_validate_bool(self):
        hocon = """
{
    active: True
}
"""

        schema_yaml = """
title: test-schema
type: object
required:
  - active
properties:
  active:
    type: float
"""
        conf = ConfigFactory.parse_string(hocon)
        schema = yaml.load(schema_yaml)
        self.assertTrue(hocon_validator.validate(schema, conf))

    def test_validate_float(self):
        hocon = """
{
    active: 2
}
"""

        schema_yaml = """
title: test-schema
type: object
required:
  - active
properties:
  active:
    type: float
"""
        conf = ConfigFactory.parse_string(hocon)
        schema = yaml.load(schema_yaml)
        self.assertTrue(hocon_validator.validate(schema, conf))

    def test_validate_string(self):
        hocon = """
{
    active: foo
}
"""

        schema_yaml = """
title: test-schema
type: object
required:
  - active
properties:
  active:
    type: string
"""
        conf = ConfigFactory.parse_string(hocon)
        schema = yaml.load(schema_yaml)
        self.assertTrue(hocon_validator.validate(schema, conf))

    def test_validate_list(self):
        hocon = """
{
    active: [1, 2, 3]
}
"""

        schema_yaml = """
title: test-schema
type: object
required:
  - active
properties:
  active:
    type: list
"""
        conf = ConfigFactory.parse_string(hocon)
        schema = yaml.load(schema_yaml)
        self.assertTrue(hocon_validator.validate(schema, conf))

    def test_validate_object(self):
        hocon = """
{
    active: {
        test: 1
    }
}
"""

        schema_yaml = """
title: test-schema
type: object
required:
  - active
properties:
  active:
    type: object
    properties:
      test:
        type: float
"""
        conf = ConfigFactory.parse_string(hocon)
        schema = yaml.load(schema_yaml)
        self.assertTrue(hocon_validator.validate(schema, conf))

    def test_validate_list2(self):
        hocon = """[1, 2, 3]
"""

        schema_yaml = """
title: test-schema
type: list
items:
  type: float
"""
        conf = ConfigFactory.parse_string(hocon)
        schema = yaml.load(schema_yaml)
        self.assertTrue(hocon_validator.validate(schema, conf))

    def test_validate_list3(self):
        hocon = '[1600, "Pennsylvania", "Avenue", "NW"]'

        schema_yaml = """
title: test-schema
type: list
items:
  - type: float
  - type: string
  - type: string
  - type: string
"""
        conf = ConfigFactory.parse_string(hocon)
        schema = yaml.load(schema_yaml)
        self.assertTrue(hocon_validator.validate(schema, conf))

    def test_validate_list5(self):
        hocon = '[{foo: True, bar: "test"}, "Pennsylvania"]'

        schema_yaml = """
title: test-schema
type: list
items:
  - type:
      object
    properties:
      foo:
        type: bool
      bar:
        type: string
  - type: string
"""
        conf = ConfigFactory.parse_string(hocon)
        schema = yaml.load(schema_yaml)
        self.assertTrue(hocon_validator.validate(schema, conf))

    def test_validate_list5(self):
        hocon = '[[1, 2, 3], ["Pennsylvania"]]'

        schema_yaml = """
title: test-schema
type: list
items:
  - type:
      list
    items:
      type: float
  - type:
      list
    items:
      type: string
"""
        conf = ConfigFactory.parse_string(hocon)
        schema = yaml.load(schema_yaml)
        self.assertTrue(hocon_validator.validate(schema, conf))
