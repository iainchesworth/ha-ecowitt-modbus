# Ecowitt Modbus for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/iainchesworth/ha-ecowitt-modbus.svg)](LICENSE)

A Home Assistant custom integration for **Fine Offset / Ecowitt** weather sensors over Modbus (typically an RTU-over-TCP serial gateway, not the sensor speaking Modbus TCP natively).

This is a community integration built on Home Assistant's shared Modbus connection (`homeassistant.components.modbus`) -- it requires a recent Home Assistant release carrying that API; see [Requirements](#requirements) below.

## Supported devices

| Device | Default address | Description |
| :----- | :-------------- | :---------- |
| WS90 | `0x90` (144) | All-in-one weather sensor array with no moving parts |
| WN69LP | `0x24` (36) | Wired 7-in-1 sensor array with a mechanical anemometer and tipping-bucket rain gauge |

These are the wired, RS-485 members of the Ecowitt range. The wireless sensors, and the gateways they report to, do not speak Modbus -- use Home Assistant's built-in [Ecowitt](https://www.home-assistant.io/integrations/ecowitt/) integration for those.

## Why not just the built-in `modbus:` YAML platform?

The legacy `modbus:` platform can already poll these sensors' raw registers, but every value comes back as an unscaled integer -- you'd need your own templates to turn a raw `662` into `26.2 °C`. This integration does that decoding for you (via [`ecowitt-modbus`](https://github.com/iainchesworth/ecowitt-modbus)), exposes proper `device_class`/`unit_of_measurement`/`state_class` metadata, and is configured through the UI rather than YAML.

## Installation

### HACS (recommended)

1. In HACS, add this repository as a custom repository (category: Integration): `https://github.com/iainchesworth/ha-ecowitt-modbus`.
2. Install "Ecowitt Modbus" from HACS.
3. Restart Home Assistant.
4. Go to **Settings -> Devices & Services -> Add Integration**, search for "Ecowitt Modbus".

### Manual

Copy `custom_components/ecowitt_modbus` into your Home Assistant `config/custom_components/` directory and restart.

## Configuration

Configuration is done entirely through the UI. You are asked for the model first, because these sensors do not report which model they are and it cannot be detected.

| Field | Description |
| --- | --- |
| Model | The model printed on the sensor, `WS90` or `WN69LP`. |
| Host | The hostname or IP address of the gateway the sensor is connected to. |
| Port | The gateway's Modbus TCP port (usually 502). |
| Device address | The sensor's Modbus device address. Defaults to the factory setting for the selected model. |

During setup the integration reads the sensor and checks the readings are consistent with the selected model. Setup does not complete unless they are.

## Entities

Both models report light, UV index, temperature, humidity, wind speed, gust speed, wind direction, rainfall, and absolute pressure.

The **WS90** adds a rain counter: the same cumulative total as rainfall, at 0.01mm instead of 0.1mm resolution. Disabled by default, since it duplicates a sensor that is already there.

The **WN69LP** adds battery voltage, supply voltage, and a second "recent rainfall" total. Supply voltage and recent rainfall are disabled by default -- the latter because the specification does not define what period it covers.

## Known limitations

The **WN69LP has no model or serial-number register**. Two things follow from that:

- Setup cannot positively confirm the model. It checks the readings fall within the ranges a weather sensor can physically produce, which rules out most unrelated devices, but it cannot distinguish a WN69LP from another device whose registers happen to decode plausibly at the same addresses.
- A WN69LP is identified by where it answers, not by what it is. A different WN69LP at the same address is indistinguishable, and its readings would be published under the original sensor's entities. Moving one to a new address is a reconfiguration, and the integration has to be told rather than working it out.

The **WS90** reports both a fixed device code and a device ID, so neither limitation applies to it: its entry is keyed on that ID and re-checks it on every poll.

Neither model's automatic reporting mode is used (this integration polls), and neither model's write commands -- rainfall reset, software reset -- are exposed as actions.

## Brand images

The device and config-flow icon/logo (`custom_components/ecowitt_modbus/brand/`) are Ecowitt's own official brand assets, reused from the [existing `ecowitt` core integration's entry](https://github.com/home-assistant/brands/tree/master/core_integrations/ecowitt) in `home-assistant/brands`. Bundled directly per the [Brands Proxy API](https://developers.home-assistant.io/blog/2026/02/24/brands-proxy-api) (Home Assistant 2026.3.0+) rather than submitted to that repository -- it no longer accepts new custom-integration brand submissions.

## Requirements

- Home Assistant 2026.9.0b0 or newer -- earlier releases don't have the shared Modbus connection API this integration depends on.
- A supported sensor reachable over Modbus RTU-over-TCP (or native Modbus TCP), typically through an RS485-to-Ethernet gateway.

The [`ecowitt-modbus`](https://pypi.org/project/ecowitt-modbus/) device library is installed automatically from PyPI as a normal requirement. Earlier versions of this integration vendored a copy of it, because it had not been published yet; that is no longer the case and the vendored copy has been removed.

## Development

Run `scripts/setup` once to install dependencies, `scripts/develop` to launch a local Home Assistant instance with this integration on the Python path, and `scripts/lint` to format and lint before committing. See [CONTRIBUTING.md](CONTRIBUTING.md) for more.

## Related projects

This is one of three repositories for Ecowitt Modbus support in Home Assistant:

* [`ecowitt-modbus`](https://github.com/iainchesworth/ecowitt-modbus) -- the standalone device library this integration depends on.
* [`ha-core-ws90`](https://github.com/iainchesworth/ha-core-ws90) -- a `home-assistant/core` fork adding the same integration as a built-in component (branch `ecowitt-ws90-integration`), for anyone who'd rather wait for it to ship in core than install a custom integration.
