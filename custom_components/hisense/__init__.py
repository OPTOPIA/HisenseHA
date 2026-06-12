from homeassistant import config_entries, core
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DEVICE_TYPE_AC, DOMAIN
from .coordinator import HisenseDataUpdateCoordinator
from .pyhisenseapi import HiSenseACClient, HiSenseDeviceClient

PLATFORMS = ["climate", "switch", "button", "number", "sensor"]


async def async_setup_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}
    
    session = async_get_clientsession(hass)
    # Setup devices based on the selected devices from the config flow
    for device_info in entry.data["devices"]:
        device_id = device_info["device_id"]
        wifi_id = device_info["wifi_id"]
        refresh_token = device_info["refresh_token"]
        device_type = device_info.get("device_type", DEVICE_TYPE_AC)
        client_class = HiSenseACClient if device_type == DEVICE_TYPE_AC else HiSenseDeviceClient
        device_name = device_info.get("device_name") or (
            "Hisense AC" if device_type == DEVICE_TYPE_AC else device_id
        )
        device_type_name = device_info.get("device_type_name") or (
            "空调" if device_type == DEVICE_TYPE_AC else ""
        )
        client = client_class(
            wifi_id=wifi_id,
            device_id=device_id,
            refresh_token=refresh_token,
            session=session,
            device_type=device_type,
            device_type_name=device_type_name,
            device_name=device_name,
        )
        coordinator = HisenseDataUpdateCoordinator(hass, client)
        await coordinator.async_config_entry_first_refresh()
        hass.data[DOMAIN][entry.entry_id][device_id] = coordinator

    # Load platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
