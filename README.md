# uyr

A silly weather app for the terminal. It works.

Fetches forecast data from met.no and displays it with badly drawn custom icons.
Tested in Kitty and Konsole.

## Dependencies

- python
- kitty (for image display)
- pipewire-pulse (for audio)

## Installation

```bash
git clone https://github.com/ViggoRomrakett/uyr.git
cd uyr
bash install.sh
```

## Usage

```bash
uyr 'location' 'number|all'
```

- `location` — any place name (e.g. oslo, bergen, york)
- `number` — hours from now (0 = current hour)
- `all` — display all available hourly forecasts

**Examples:**
```bash
uyr oslo 0        # current weather in Oslo
uyr bergen all    # full forecast for Bergen
```

## Notes

Uses the [met.no API](https://api.met.no) for weather data and
[Nominatim](https://nominatim.openstreetmap.org) for location lookup.
