[![GitHub Release][releases-shield]][releases]
[![Total downloads][total-downloads-shield]][total-downloads]
[![Latest release downloads][latest-release-downloads-shield]][latest-release-downloads]

<p align="right">
<img width="250" alt="Logo" src="https://raw.githubusercontent.com/toringer/home-assistant-heru/master/assets/logo.png">
</p>

# HERU energy recovery unit component for Home Assistant


Control and monitor your Östberg HERU energy recovery unit from Home Assistant through the onboard modbus interface.

<p align="center">
<img width="250" alt="Sensors" src="https://raw.githubusercontent.com/toringer/home-assistant-heru/master/assets/sensors.png"><img width="250" alt="Controls" src="https://raw.githubusercontent.com/toringer/home-assistant-heru/master/assets/controls.png"><img width="250" alt="Diagnostic" src="https://raw.githubusercontent.com/toringer/home-assistant-heru/master/assets/diagnostic.png">
</p>


*__Note__: The integrations requires HERU firmware version 1.09i or newer. Version 1.09i introduced one decimal to temperature sensors, and therefore needs to be scaled.*

### Sensors
| Sensor  | Modbus register |
| ------------- | ------------- |
|Boost input|1x00002|
|Current exhaust fan power|3x00026|
|Current exhaust fan step|3x00024|
|Current heating power|3x00029|
|Current heat/cold recovery power|3x00030|
|Current supply fan power|3x00025|
|Current supply fan step|3x00023|
|Exhaust air temperature|3x00005|
|Exhaust fan alarm|1x00022|
|Extract air temperature|3x00004|
|Filter days left|3x00020|
|Filter timer alarm|1x00025|
|Fire alarm|1x00010|
|Heat recovery temperature|3x00007|
|Outdoor temperature | 3x00002  |
|Overpressure input|1x00003|
|Rotor alarm|1x00011|
|Supply air temperature|3x00003|
|Supply fan alarm|1x00021|


### Buttons
| Button  | Modbus register |
| ------------- | ------------- |
| Clear Alarms |0x00005|
|Reset filter timer|0x00006|
|Sync date and time|4x00400 - 4x00405|


### Switches
| Switch  | Modbus register |
| ------------- | ------------- |
|Away mode|0x00004|
|Boost mode|0x00003|
|Heater enabled|4x00067|
|Overpressure mode|0x00002|
|Preheater enabled|4x00064|



## Installation

### HACS
1. In Home Assistant go to HACS -> Integrations. Click on "+ Explore & Download Repositories" and search for "HERU".

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=toringer&repository=home-assistant-heru&category=integration)

2. In Home Assistant go to Settings -> Devices & Services -> Integrations. Click on "+ Add integration" and search for "HERU".

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=heru)


## Configuration HERU unit

Enable modbus and network on the HERU unit in the service menu using `1991` as pin code.



[releases-shield]: https://img.shields.io/github/v/release/toringer/home-assistant-heru?style=flat-square
[releases]: https://github.com/toringer/home-assistant-heru/releases
[total-downloads-shield]: https://img.shields.io/github/downloads/toringer/home-assistant-heru/total?style=flat-square
[total-downloads]: https://github.com/toringer/home-assistant-heru
[latest-release-downloads-shield]: https://img.shields.io/github/downloads/toringer/home-assistant-heru/latest/total?style=flat-square
[latest-release-downloads]: https://github.com/toringer/home-assistant-heru
