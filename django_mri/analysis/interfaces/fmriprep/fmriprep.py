"""
Definition of the
:class:`~django_mri.analysis.interfaces.fmriprep.fmriprep` interface.
"""

import os
from pathlib import Path


class fMRIprep:
    """
    An interface for the *fMRIPrep* preprocessing pipeline.

    References
    ----------
    * fmriprep_

    .. _fmriprep:
       https://fmriprep.org/en/stable/index.html
    """

    #: "Flags" indicate parameters that are specified without any arguments,
    #: i.e. they are a switch for some binary configuration.
    FLAGS = (
        "align_seepi",
        "rpe_none",
        "rpe_pair",
        "rpe_all",
        "rpe_header",
        "force",
        "quiet",
        "info",
        "nocleanup",
    )

    #: Non-default output configuration.
    SUPPLEMENTARY_OUTPUTS = ["eddyqc_all"]
    DEFAULT_INPUTS = ["json_import", "fslgrad"]
    #: Default name for primary output file.
    DEFAULT_OUTPUT_NAME = "preprocessed_dwi.mif"

    #: *eddy* output files by key.
    #:
    #: References
    #: ----------
    #: * eddy_
    #:
    #: .. _eddy:
    #:    https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/eddy
    EDDY_OUTPUTS = {
        "out_movement_rms": "eddy_movement_rms",
        "eddy_mask": "eddy_mask.mif",
        "out_outlier_map": "eddy_outlier_map",
        "out_outlier_n_sqr_stdev_map": "eddy_outlier_n_sqr_stdev_map",
        "out_outlier_n_stdev_map": "eddy_outlier_n_stdev_map",
        "out_outlier_report": "eddy_outlier_report",
        "out_parameter": "eddy_parameters",
        "out_restricted_movement_rms": "eddy_restricted_movement_rms",
        "out_shell_alignment_parameters": "eddy_post_eddy_shell_alignment_parameters",  # noqa: E501
        "out_shell_pe_translation_parameters": "eddy_post_eddy_shell_PE_translation_parameters",  # noqa: E501
    }

    __version__ = "BETA"

    def __init__(self, **kwargs):
        self.configuration = kwargs

    def add_supplementary_outputs(self, destination: Path) -> dict:
        """
        Adds the *eddy* output files to the interface's configuration before
        generating the command to run.

        References
        ----------
        * eddy_

        .. _eddy:
            https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/eddy

        Parameters
        ----------
        destination : Path
            Output directory

        Returns
        -------
        dict
            Updated configuration dictionary
        """

        config = self.configuration.copy()
        for key in self.SUPPLEMENTARY_OUTPUTS:
            if key not in config.keys():
                config[key] = destination
        return config

    def set_configuration_by_keys(self, config: dict):
        key_command = ""
        for key, value in config.items():
            key_addition = f" -{key}"
            if isinstance(value, list):
                for val in value:
                    key_addition += f" {val}"
            elif key in self.FLAGS and value:
                pass
            else:
                key_addition += f" {value}"
            key_command += key_addition
        return key_command

    def generate_command(self, destination: Path, config: dict) -> str:
        """
        Returns the command to be executed in order to run the analysis.

        Parameters
        ----------
        destination : Path
            Output files destination direcotry
        config : dict
            Configuration arguments for the command

        Returns
        -------
        str
            Complete execution command
        """

        output_path = destination / self.DEFAULT_OUTPUT_NAME
        scan = config.pop("scan")
        command = f"dwifslpreproc {scan} {output_path}"
        return command + self.set_configuration_by_keys(config)

    def generate_output_dict(self, destination: Path) -> dict:
        """
        Generates a dictionary of the expected output file paths by key.

        Parameters
        ----------
        destination : Path
            Output files destination directory

        Returns
        -------
        dict
            Output files by key
        """

        output_dict = {
            "preprocessed_dwi": destination / self.DEFAULT_OUTPUT_NAME,
        }
        for key, value in self.EDDY_OUTPUTS.items():
            output_dict[key] = destination / value
        return output_dict

    def run(self, destination: Path = None) -> dict:
        """
        Runs *dwifslpreproc* with the provided *scan* as input.
        If *destination* is not specified, output files will be created within
        *scan*\'s directory.

        Parameters
        ----------
        scan : ~django_mri.models.scan.Scan
            Input scan
        destination : Path, optional
            Output files destination directory, by default None

        Returns
        -------
        dict
            Output files by key

        Raises
        ------
        RuntimeError
            Run failure
        """

        destination = Path(destination) if destination else scan.path.parent
        config = self.add_supplementary_outputs(destination)
        command = self.generate_command(destination, config)
        raise_exception = os.system(command)
        if raise_exception:
            raise RuntimeError(
                f"Failed to run dwifslpreproc!\nExecuted command: {command}"
            )
        return self.generate_output_dict(destination)
