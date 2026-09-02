# Ecowitt WS90 for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/iainchesworth/ha-ecowitt-ws90.svg)](LICENSE)

A Home Assistant custom integration for the **Fine Offset / Ecowitt WS90** all-in-one weather sensor over Modbus (typically an RTU-over-TCP serial gateway, not the sensor speaking Modbus TCP natively).

This is a community integration built on Home Assistant's shared Modbus connection (`homeassistant.components.modbus`) -- it requires a recent Home Assistant release carrying that API; see [Requirements](#requirements) below.

## Why not just the built-in `modbus:` YAML platform?

The legacy `modbus:` platform can already poll a WS90's raw registers, but every value comes back as an unscaled integer -- you'd need your own templates to turn a raw `662` into `26.2 °C`. This integration does that decoding for you (via [`ecowitt-ws90-modbus`](https://github.com/iainchesworth/ecowitt-ws90-modbus), vendored into this repository -- see [Vendoring](#vendoring) below), exposes proper `device_class`/`unit_of_measurement`/`state_class` metadata, and is configured through the UI rather than YAML.

## Installation

### HACS (recommended)

1. In HACS, add this repository as a custom repository (category: Integration): `https://github.com/iainchesworth/ha-ecowitt-ws90`.
2. Install "Ecowitt WS90" from HACS.
3. Restart Home Assistant.
4. Go to **Settings -> Devices & Services -> Add Integration**, search for "Ecowitt WS90".

### Manual

Copy `custom_components/ecowitt_ws90` into your Home Assistant `config/custom_components/` directory and restart.

## Configuration

Configuration is done entirely through the UI:

| Field | Description |
| --- | --- |
| Host | The WS90's Modbus gateway hostname or IP address. |
| Port | The gateway's Modbus TCP port (usually 502). |
| Unit ID | The WS90's Modbus device address (factory default `0x90` / 144). |

The integration probes the device during setup and will not let you finish adding an entry unless a WS90 actually answers.

## Entities

Ten sensor entities are created, all under one device: light, UV index, temperature, humidity, wind speed, gust speed, wind direction, rainfall, absolute pressure, and a finer-resolution rain counter (disabled by default -- it's the same cumulative rain total as "rainfall", just at 0.01mm instead of 0.1mm resolution).

## Vendoring

The [`ecowitt-ws90-modbus`](https://github.com/iainchesworth/ecowitt-ws90-modbus) device library -- which knows nothing about Home Assistant and could be reused by any Python project -- is copied into `custom_components/ecowitt_ws90/vendor/` rather than installed from PyPI. This keeps the integration installable via HACS without waiting on a PyPI release; once the library has a stable release, a future version of this integration may switch to a normal `requirements` dependency instead.

## Requirements

- Home Assistant 2026.9.0 or newer (or the current `dev`/beta build until that release ships stable) -- earlier releases don't have the shared Modbus connection API this integration depends on.
- A WS90 reachable over Modbus RTU-over-TCP (or native Modbus TCP), typically through an RS485-to-Ethernet gateway.

## Development

Run `scripts/setup` once to install dependencies, `scripts/develop` to launch a local Home Assistant instance with this integration on the Python path, and `scripts/lint` to format and lint before committing. See [CONTRIBUTING.md](CONTRIBUTING.md) for more.

## Related projects

This is one of three repositories for WS90 support in Home Assistant:

* [`ecowitt-ws90-modbus`](https://github.com/iainchesworth/ecowitt-ws90-modbus) -- the standalone device library this integration vendors.
* [`ha-core-ws90`](https://github.com/iainchesworth/ha-core-ws90) -- a `home-assistant/core` fork adding the same integration as a built-in component (branch `ecowitt-ws90-integration`), for anyone who'd rather wait for it to ship in core than install a custom integration.
