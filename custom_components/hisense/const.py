"""Constants for HiSense Integration."""
DOMAIN = "hisense"

# Configuration keys
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

DEVICE_TYPE_AC = "ac"
DEVICE_TYPE_WASHER = "washer"
DEVICE_TYPE_PROJECTOR = "projector"
DEVICE_TYPE_UNKNOWN = "unknown"

SUPPORTED_DEVICE_KEYWORDS = {
    "空调": DEVICE_TYPE_AC,
    "洗衣机": DEVICE_TYPE_WASHER,
    "投影仪": DEVICE_TYPE_PROJECTOR,
}


def climate_limits_signal(device_id: str) -> str:
    """Dispatcher signal when per-device climate min/max limits change."""
    return f"{DOMAIN}_climate_limits_{device_id}"


def device_suggested_object_id(device_id: str, suffix: str) -> str:
    """Suggested entity object_id segment: slugified device id + role (for new entities)."""
    from homeassistant.util import slugify

    return f"{slugify(device_id)}_{suffix}"
