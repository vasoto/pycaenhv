# Configuration

Using the `hvconfig` script, CAEN HV modules can be setup automatically using a configuration file. The format of the configuration file is `.toml` and its structure should be the following:

## Example

The following example configuration will configure a single `V65XX` module, referneced as `test`, on address `0_0_00000000`, connected through an `USB` port.
Channel *1* voltage will be set to 500V and the current will be 1 mA. The voltage for all other channels will be set to 350V and current to 500 uA.

```toml
[hv]
[hv.test]
board = "V65XX"
link = "USB"
address = "0_0_00000000"
[hv.test.channels]
[hv.test.channels.default]
VSet=350
ISet=500
[hv.test.channels.channel.1]
VSet=500
ISet=1000
```

## `hv`*

#### (Mandatory)

Holds information about all HV boards.

## `hv.<NAME>`*

#### (Mandatory)

Configuration for board "NAME".


### `board`*

#### (Mandatory)

Board type. Should be one of:

* SY1527
* SY2527
* SY4527
* SY5527
* N568
* V65XX
* N1470
* V8100
* N568E
* DT55XX
* FTK
* DT55XXE
* N1068
* SMARTHV
* NGPS

### `link`*

#### (Mandatory)

Link type. Should be one of:

* TCPIP
* RS232
* CAENET
* USB
* OPTLINK
* USB_VCP


### `address`*

#### (Mandatory)

Address information of the board. Depends on the link type.

### `user`

#### (Optional)

User name of the module. Use only if it is set.

### `password`

#### (Optional)

Password. Used in combination with `user`.

## `hv.<NAME>.channels`

Channels configuration. 

## `hv.<NAME>.channels.default`

#### (Optional)

Default values for all channels, except those specified in `hv.<NAME>.channels.channel` section.

User can set all the `R/W` or `W` properties for a given module's channels by using their name.

For example:

* `VSet` will set the voltage
* `ISet` will set the current

## `hv.<NAME>.channels.channel.<NUMBER>`

Set properties for a specific channel __NUMBER__ in module __NAME__.  __NUMBER__ should be a number in the allowed range of channels for the given module.

User can set all the `R/W` or `W` properties for a given module's channels by using their name.

For example:

* `VSet` will set the voltage
* `ISet` will set the current
