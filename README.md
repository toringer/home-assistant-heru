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
