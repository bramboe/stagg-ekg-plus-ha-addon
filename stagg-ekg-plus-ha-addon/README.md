# Fellow Stagg EKG Pro (WiFi) – Home Assistant Custom Integration

Home Assistant **custom integration** for the Fellow Stagg EKG Pro using the kettle’s **HTTP CLI API only** (no Bluetooth, no HACS). When the kettle is on the same network, it can show up automatically via discovery. Aligned with the [Home Assistant integration quality scale](https://www.home-assistant.io/docs/quality_scale/) for **Platinum** tier.

---

## Installation (custom integration only)

1. Copy the `custom_components/fellow_stagg` folder into your Home Assistant **custom_components** directory (e.g. `config/custom_components/fellow_stagg`).
2. Restart Home Assistant.
3. Go to **Settings → Devices & Services → Add Integration** and search for **Fellow Stagg EKG Pro (WiFi)**.

---

## Adding the integration

- **Discovery (same network)**  
  If your kettle is on the same LAN and advertises via mDNS (`_http._tcp`), it may appear under **Discovered**. You can also add the integration manually and check **Discover on network** to scan your LAN for kettles.
- **Manual**  
  Enter the kettle’s base URL (e.g. `http://192.168.1.32`). The `/cli` path is added automatically.

---

## Supported devices and requirements

- **Compatible:** Fellow Stagg EKG Pro with firmware that exposes the HTTP CLI (e.g. `setstate`, `setsetting settempr`, `/cli?cmd=state`).
- **Network:** Kettle and Home Assistant must be on the same network (WiFi or wired).
- **No Bluetooth or HACS** required.

---

## What this integration provides

### Entities and platforms

- **Water heater** – Main entity for power and target temperature.
- **Switch** – Power, Sync clock, Live heating graph (optional 1 s polling for graph).
- **Number** – Target temperature, Schedule temperature.
- **Select** – Schedule mode (off / once / daily), Clock display mode (off / digital / analog).
- **Time** – Schedule time (when the kettle should start).
- **Button** – Update schedule (pushes current schedule settings to the kettle).
- **Sensors** – Power, Current temperature, Target temperature, Hold mode, Kettle position, Clock, Schedule mode, Water stabilized (PID stability).

### Services

- `fellow_stagg.set_schedule` – Set schedule time, temperature, and enable/disable.
- `fellow_stagg.disable_schedule` – Disable schedule.
- `fellow_stagg.update_schedule` – Apply current schedule time/temp/mode from entities to the kettle.

See **Developer tools → Services** and **Settings → Devices & Services → Fellow Stagg → … → Services** for parameters.

---

## How data is updated

- **Polling:** The integration polls the kettle every **5 seconds** (configurable via `POLLING_INTERVAL_SECONDS` in `const.py`) for state, settings, and schedule. This keeps network and CPU usage predictable (efficient data handling, Platinum).
- **Live heating graph:** When the “Live heating graph” switch is on, an additional **1 s** poll runs for PID data used by the heating graph card. Turn the switch off when not needed to reduce load.

---

## Reconfiguration and diagnostics

- **Reconfigure:** From **Settings → Devices & Services → Fellow Stagg → … (your device) → Configure**, you can change the kettle base URL. The integration reloads with the new URL.
- **Diagnostics:** From the same device menu, use **Download diagnostics** to get a snapshot of the config entry and last coordinator data (for troubleshooting).

---

## Discovery behaviour

1. **Zeroconf**  
   If the kettle advertises an HTTP service (`_http._tcp.local.`), Home Assistant may discover it. The integration checks that the device responds to `/cli?cmd=state` with Fellow Stagg–style output before offering it.
2. **Discover on network**  
   In the config flow, checking **Discover on network** scans your local subnet(s) (from HA’s network adapters, or fallback to common ranges like 192.168.0.0/24, 192.168.1.0/24, 10.0.0.0/24) and probes each IP for the kettle CLI. Any host that responds with the expected state is listed so you can add it.

---

## Example use cases

- **Morning routine:** Set a schedule (e.g. 07:30, 95 °C) so water is ready when you get up.
- **Tea/coffee:** Use the water heater or target temperature number to heat to a set temperature and turn off.
- **Dashboard:** Add the water heater card, temperature sensors, and the optional [Fellow Stagg Heating Graph](custom_components/fellow_stagg/www/HEATING_GRAPH_CARD.md) card for live temperature and PID view.
- **Automations:** Use `water_heater.turn_on` / `turn_off`, or services like `fellow_stagg.set_schedule` and `fellow_stagg.disable_schedule` in automations or scripts.

---

## Troubleshooting

| Issue | What to try |
|-------|---------------------|
| Integration won’t add / “Could not connect” | Check the base URL (e.g. `http://192.168.1.32`). Ensure the kettle is on and on the same network. Open `http://<kettle-ip>/cli?cmd=state` in a browser; you should see text with `mode=`, `tempr`, etc. |
| Entities show “unavailable” | Kettle may be off or unreachable. Check network and power. After a short time, the coordinator will retry and entities should recover when the kettle responds again. |
| No devices found when discovering | Ensure the kettle is on and its firmware supports the HTTP CLI. Try manual entry with the kettle’s IP. If you use a non-standard subnet, manual entry is more reliable than scan. |
| Schedule doesn’t stick | Use the **Update schedule** button after changing schedule time, temperature, or mode. For automations, call `fellow_stagg.update_schedule` after changing entities if needed. |

---

## Removal

1. **Settings → Devices & Services → Fellow Stagg**
2. Select the device → **…** → **Delete**
3. Remove the `custom_components/fellow_stagg` folder and restart Home Assistant if you uninstall the integration completely.

---

## Running tests

Bronze/Gold: automated tests cover the config flow. To run them:

```bash
pip install -r requirements_test.txt
pytest tests/
```

Requires [pytest-homeassistant-custom-component](https://github.com/MatthewFlamm/pytest-homeassistant-custom-component) for the `hass` fixture and custom integration loading.

---

## Quality scale and credits

This integration is structured to meet the [Platinum](https://www.home-assistant.io/docs/quality_scale/#-platinum) tier: fully async, typed, coordinator-based polling, UI config flow with discovery and reconfiguration, diagnostics, translations, and tests. Rule tracking: `custom_components/fellow_stagg/quality_scale.yaml`.

Originally based on [levi/stagg-ekg-plus](https://github.com/levi/stagg-ekg-plus) and since substantially rewritten. This version is WiFi-only, with no Bluetooth and no HACS dependency, and adds discovery and reconfiguration so devices on the same network can show up and be reconfigured from the UI.
