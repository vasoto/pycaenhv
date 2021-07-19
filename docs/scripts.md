# Scripts

## caenhv

Command line tool for CAEN HV modules.

## hvconfig

Configure one or many CAEN HV modules using a `.toml` configuration file.

```bash
hvconfig config.toml
```

### Usage

```bash
usage: hvconfig [-h] [--verbose] [-on | -off] CONFIGFILE

Configure CAEN HV Modules

positional arguments:
  CONFIGFILE

optional arguments:
  -h, --help  show this help message and exit
  --verbose   verbose flag
  -on
  -off
```

### Turn module ON/OFF

This command can be used to turn or on off the modules declared in the configuration file. this can be done by using the `-on` or `-off` arguments.