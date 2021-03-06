# hocon-validator

[![Build Status](https://travis-ci.org/chezou/hocon-validator.svg?branch=master)](https://travis-ci.org/chezou/hocon-validator)

HOCON validator, inspired by [JSON schema](http://json-schema.org/).

If you can write schema file with YAML, you can validate your HOCON file.

## Requirements

- pyyaml
- pyhocon

For developpers:

```
$ pip install -r requirements.txt -c constraints.txt
```

## USAGE

Install with pip:

```
$ pip install hocon-validator
```

You can run as follows:

```
$ hocon-validator.py [-h] hocon_file schema_file.yml
```

Example:

OK pattern

```
$ python hocon-validator.py ./examples/tableau-impala-demo-cluster.conf ./examples/etableau-schema.yml

HOCON file: ./examples/tableau-impala-demo-cluster.conf
Schema file: ./examples/tableau-schema.yml

Start validation...
All required fields has passed!
```

NG pattern

```
$ python hocon-validator.py ./examples/tableau-impala-demo-cluster.conf ./examples/etableau-schema.yml

HOCON file: ./examples/tableau-impala-demo-cluster.conf
Schema file: ./examples/tableau-schema.yml

Start validation...
accessKeyId does not exist or is not a string value.
secretAccessKey does not exist or is not a string value.
```

## Schema

See `./examples/tableau-schema.yml` for example.
