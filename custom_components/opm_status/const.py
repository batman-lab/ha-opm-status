"""Constants for the OPM Status integration."""

DOMAIN = "opm_status"

CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 15  # minutes

API_URL = "https://www.opm.gov/json/operatingstatus.json"

ATTR_TITLE = "title"
ATTR_LOCATION = "location"
ATTR_STATUS_SUMMARY = "status_summary"
ATTR_SHORT_MESSAGE = "short_message"
ATTR_LONG_MESSAGE = "long_message"
ATTR_EXTENDED_INFO = "extended_information"
ATTR_APPLIES_TO = "applies_to"
ATTR_ICON = "icon"
ATTR_STATUS_TYPE = "status_type"
ATTR_DATE_POSTED = "date_posted"
ATTR_URL = "url"
