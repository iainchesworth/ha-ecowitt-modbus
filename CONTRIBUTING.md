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

launches a local Home Assistant instance with `custom_components/` on the Python path, so `ecowitt_modbus` loads as if it had been installed normally. Add it via **Settings -> Devices & Services** as usual.

## Before opening a pull request

```bash
scripts/lint
```

formats and lints the codebase with Ruff. CI also runs `hassfest` and the HACS repository validator (`.github/workflows/validate.yml`) -- both are worth checking locally if you can.

Anything to do with register maps, decoding, or device behaviour belongs in the [`ecowitt-modbus`](https://github.com/iainchesworth/ecowitt-modbus) device library rather than here -- this repository holds only the Home Assistant plumbing. Change the library first, release it, then bump the pin in `manifest.json`.

The integration source here is kept byte-identical to the copy proposed for `home-assistant/core` ([#181083](https://github.com/home-assistant/core/pull/181083)), so that the two cannot drift while that review is open. If you change a `.py` file here, make the same change there.
