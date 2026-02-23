# OPM Federal Operating Status - Home Assistant Integration

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![Validate with HACS](https://github.com/batman-lab/ha-opm-status/actions/workflows/validate.yml/badge.svg)](https://github.com/batman-lab/ha-opm-status/actions/workflows/validate.yml)
[![Validate with hassfest](https://github.com/batman-lab/ha-opm-status/actions/workflows/hassfest.yml/badge.svg)](https://github.com/batman-lab/ha-opm-status/actions/workflows/hassfest.yml)

A Home Assistant custom integration that monitors the **U.S. Office of Personnel Management (OPM)** federal government operating status for the Washington, DC area.

This is especially useful for federal employees, contractors, and anyone whose schedule is affected by federal office closures due to weather, emergencies, or other events.

## Features

- **Operating Status Sensor** (`sensor.opm_federal_operating_status_operating_status`)
  The current status (e.g., "Open", "Closed", "Open - 2 hours Delayed Arrival - With Option for Unscheduled Leave or Unscheduled Telework"). Full details are available as attributes.

- **Status Message Sensor** (`sensor.opm_federal_operating_status_status_message`)
  The short human-readable message from OPM.

- **Federal Offices Open Binary Sensor** (`binary_sensor.opm_federal_operating_status_federal_offices_open`)
  `on` when offices are open (including delayed arrivals), `off` when closed.

- Configurable polling interval (default: 15 minutes)
- UI-based setup via the Integrations page (config flow)
- All data sourced from the [official OPM JSON API](https://www.opm.gov/json/operatingstatus.json)

## Installation

### HACS (Recommended)

1. Open **HACS** in your Home Assistant instance.
2. Click the **⋮** menu (top right) → **Custom repositories**.
3. Add this repository URL: `https://github.com/batman-lab/ha-opm-status`
4. Select **Integration** as the category and click **Add**.
5. Search for **OPM Federal Operating Status** in HACS and click **Download**.
6. **Restart Home Assistant.**
7. Go to **Settings → Devices & Services → Add Integration** and search for **OPM Federal Operating Status**.

Or click this button to add the repository directly:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=batman-lab&repository=ha-opm-status&category=integration)

### Manual

1. Copy the `custom_components/opm_status` directory to your `<config>/custom_components/` folder:

```
<config>/
  custom_components/
    opm_status/
      __init__.py
      binary_sensor.py
      config_flow.py
      const.py
      coordinator.py
      manifest.json
      sensor.py
      strings.json
      translations/
        en.json
```

2. Restart Home Assistant.
3. Go to **Settings → Devices & Services → Add Integration** and search for **OPM Federal Operating Status**.

## Configuration

During setup you can configure:

| Option | Default | Description |
|--------|---------|-------------|
| Update interval | 15 min | How often to poll OPM (5–120 minutes) |

You can change the interval later via **Options** on the integration card.

## Sensor Attributes

The main **Operating Status** sensor exposes these attributes:

| Attribute | Description |
|-----------|-------------|
| `title` | Full title of the status announcement |
| `location` | Geographic area (typically "Washington, DC area") |
| `status_summary` | Summary status string |
| `short_message` | Short human-readable message |
| `long_message` | Full detailed message with instructions |
| `extended_information` | Additional guidance for employees |
| `applies_to` | Date the status applies to |
| `icon` | OPM icon type (Open, Closed, Alert) |
| `status_type` | Detailed status type description |
| `date_posted` | When the status was last updated (ISO 8601) |
| `url` | Link to the OPM status page |

## Example Automations

### Send a notification when offices close

```yaml
automation:
  - alias: "OPM Status Change Notification"
    trigger:
      - platform: state
        entity_id: sensor.opm_federal_operating_status_operating_status
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🏛️ Federal Office Status Changed"
          message: "{{ state_attr('sensor.opm_federal_operating_status_operating_status', 'short_message') }}"
```

### Alert only when offices are NOT open

```yaml
automation:
  - alias: "Federal Offices Closed Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.opm_federal_operating_status_federal_offices_open
        to: "off"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🚨 Federal Offices Closed"
          message: >
            {{ states('sensor.opm_federal_operating_status_operating_status') }}
```

### Dashboard card example

```yaml
type: entities
title: Federal Operating Status
entities:
  - entity: binary_sensor.opm_federal_operating_status_federal_offices_open
  - entity: sensor.opm_federal_operating_status_operating_status
  - entity: sensor.opm_federal_operating_status_status_message
```

## Data Source

All data comes from the official OPM API:
`https://www.opm.gov/json/operatingstatus.json`

No API key is required. See the [OPM Developer Documentation](https://www.opm.gov/developer/documentation/current-status-api/) for details.
