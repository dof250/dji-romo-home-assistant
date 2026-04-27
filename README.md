# DJI Romo Home Assistant Integration

Custom Home Assistant integration for the DJI Romo robot vacuum. It is designed as a HACS-compatible custom component and builds on the credential extraction work documented here:

![DJI Romo](dji.png)

- [xn0tsa/dji-home-credential-extractor](https://github.com/xn0tsa/dji-home-credential-extractor)

## What works today

- Config flow in Home Assistant
- Creates:
  - 1 vacuum entity
  - sensors for battery, firmware, dock state, tanks, consumables, cleaning solution, and settings
  - buttons for DJI Home cleaning shortcuts/presets
- Supports start, pause, stop, return to dock, and preset cleaning through DJI Home REST endpoints

## Install through HACS

1. Put this repository on GitHub.
2. In HACS, add it as a custom repository of type `Integration`.
3. Install `DJI Romo`.
4. Restart Home Assistant.
5. Add the integration from `Settings -> Devices & Services`.

## Getting credentials

Use the extractor project to retrieve the token and serial number:

1. Follow the instructions in [dji-home-credential-extractor](https://github.com/xn0tsa/dji-home-credential-extractor)
2. Add the Home Assistant integration
3. Paste the full `.env` or `dji_credentials.txt` output into the credentials field

The config flow will parse:

- `DJI_USER_TOKEN`
- `DJI_DEVICE_SN`
- `DJI_API_URL`
- `DJI_LOCALE`

You can still enter the token and serial manually if you prefer.
