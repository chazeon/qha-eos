# QHA EOS

An EOS calculation program using QHA.

This also serve as an example of QHA Plugin.

## How to Use

The QHA EOS is currently supports tabular and JSON input.

### As an plugin for QHA

For JSON input, the command is
```sh
qha eos --json [filename]
```
for tabular input, the command is
```sh
qha eos --txt [filename]
```

### As a standalone program (not really)

For JSON input, the command is
```sh
qha-eos --json [filename]
```
for tabular input, the command is
```sh
qha-eos --txt [filename]
```

### As a Python module

For JSON input, the command is
```sh
python -m qha_eos --json [filename]
```
for tabular input, the command is
```sh
python -m qha_eos --txt [filename]
```