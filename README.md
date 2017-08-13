# hocon-validator

## Requirements

- pyyaml
- pyhocon

```
$ pip install -r requirements.txt -c constraints.txt
```

## USAGE

```
$ hocon-validator.py [-h] hocon_file schema_file
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
