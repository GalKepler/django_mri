"""
A module storing strings used to display messages.
"""

NO_DCM2NIIX = "Could not call dcm2niix! Please check settings configuration."
DCM2NIIX_FAILURE = "Failed to create NIfTI file using dcm2niix! Please check application configuration.\nDICOM directory:\t{path}\nDestination:\t{destination}\nDCM2NIIX return value:\t{returned}"
DCM2NIIX_PATH_MISMATCH = "Returned NIfTI path does not match expected destination.\nThis could indicate a problem with the conversion.\nExpected:{expected_path}\nReturned:{returned_path}"

# flake8: noqa: E501
