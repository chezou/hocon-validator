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
        type: string
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
