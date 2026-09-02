# Contributing

Contributions are welcome, whether that's a bug report, a feature request, or a pull request.

## Reporting bugs

Open an issue using the bug report template. Include your Home Assistant version, debug logs (see `config/configuration.yaml` for how this repository's dev environment enables them), and steps to reproduce -- issues without reproduction steps are much harder to act on.

## Setting up a development environment

The easiest path is the included dev container (VS Code: "Reopen in Container"), which runs `scripts/setup` for you automatically. Without a dev container:

```bash
scripts/setup
```

installs this repository's Python dependencies, including a pinned Home Assistant release matching the `homeassistant` key in `hacs.json`.

## Testing your change

```bash
scripts/develop
```

launches a local Home Assistant instance with `custom_components/` on the Python path, so `ecowitt_ws90` loads as if it had been installed normally. Add it via **Settings -> Devices & Services** as usual.

## Before opening a pull request

```bash
scripts/lint
```

formats and lints the codebase with Ruff. CI also runs `hassfest` and the HACS repository validator (`.github/workflows/validate.yml`) -- both are worth checking locally if you can.

If your change touches `custom_components/ecowitt_ws90/vendor/ecowitt_ws90_modbus/`, please make the equivalent change in [`ecowitt-ws90-modbus`](https://github.com/iainchesworth/ecowitt-ws90-modbus) first and then re-vendor it here, rather than letting the two drift apart.
