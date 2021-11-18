"""
Input and output specification dictionaries for MRtrix's *dwifslpreproc*
script.

See Also
--------
* :class:`~django_mri.analysis.interfaces.mrtrix3.dwifslpreproc.DwiFslPreproc`

Notes
-----
For more information, see MRtrix3's `dwifslpreproc reference`_.

.. _dwifslpreproc reference:
   https://mrtrix.readthedocs.io/en/latest/reference/commands/dwifslpreproc.html
"""

from django_analyses.models.input.definitions import (BooleanInputDefinition,
                                                      DirectoryInputDefinition,
                                                      FileInputDefinition,
                                                      FloatInputDefinition,
                                                      IntegerInputDefinition,
                                                      ListInputDefinition,
                                                      StringInputDefinition)
from django_analyses.models.output.definitions import FileOutputDefinition

#: *DwiFslPreproc* input specification dictionary.
DWIFSLPREPROC_INPUT_SPECIFICATION = {
    "scan": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input DWI image.",
        "is_configuration": False,
    },
    "destination": {
        "type": DirectoryInputDefinition,
        "description": "Run output destination.",
        "required": False,
        "is_configuration": False,
        "is_output_directory": True,
        "run_method_input": True,
    },
    "pe_dir": {
        "type": StringInputDefinition,
        "description": "Manually specify the phase encoding direction of the input series",  # noqa: E501
        "choices": [
            "rl",
            "lr",
            "ap",
            "pa",
            "is",
            "si",
            "-0",
            "0",
            "-1",
            "1",
            "-2",
            "2",
            "i",
            "i-",
            "j",
            "j-",
            "k",
            "k-",
        ],
    },
    "readout_time": {
        "type": FloatInputDefinition,
        "description": "Manually specify the total readout time of the input series (in seconds)",  # noqa: E501
    },
    "se_epi": {
        "type": FileInputDefinition,
        "description": "Provide an additional image series consisting of spin-echo EPI images, which is to be used exclusively by topup for estimating the inhomogeneity field (i.e. it will not form part of the output image series)",  # noqa: E501
    },
    "align_seepi": {
        "type": BooleanInputDefinition,
        "description": "Achieve alignment between the SE-EPI images used for inhomogeneity field estimation, and the DWIs (more information in Description section)",  # noqa: E501
    },
    "json_import": {
        "type": FileInputDefinition,
        "description": "Import image header information from an associated JSON file (may be necessary to determine phase encoding information)",  # noqa: E501
    },
    "topup_options": {
        "type": StringInputDefinition,
        "description": "Manually provide additional command-line options to the topup command (provide a string within quotation marks that contains at least one space, even if only passing a single command-line option to topup)",  # noqa: E501
    },
    "eddy_options": {
        "type": StringInputDefinition,
        "description": "Manually provide additional command-line options to the eddy command (provide a string within quotation marks that contains at least one space, even if only passing a single command-line option to eddy)",  # noqa: E501
    },
    "eddy_mask": {
        "type": FileInputDefinition,
        "description": "Provide a processing mask to use for eddy, instead of having dwifslpreproc generate one internally using dwi2mask",  # noqa: E501
    },
    "eddy_slspec": {
        "type": FileInputDefinition,
        "description": "Provide a file containing slice groupings for eddy’s slice-to-volume registration",  # noqa: E501
    },
    "eddyqc_text": {
        "type": StringInputDefinition,
        "description": "Copy the various text-based statistical outputs generated by eddy, and the output of eddy_qc (if installed), into an output directory",  # noqa: E501
        "is_output_path": True,
    },
    "eddyqc_all": {
        "type": StringInputDefinition,
        "description": "Copy ALL outputs generated by eddy (including images), and the output of eddy_qc (if installed), into an output directory",  # noqa: E501
        "is_output_path": True,
    },
    "rpe_none": {
        "type": BooleanInputDefinition,
        "description": "Specify that no reversed phase-encoding image data is being provided; eddy will perform eddy current and motion correction only",  # noqa: E501
    },
    "rpe_pair": {
        "type": BooleanInputDefinition,
        "description": "Specify that a set of images (typically b=0 volumes) will be provided for use in inhomogeneity field estimation only (using the -se_epi option)",  # noqa: E501
    },
    "rpe_all": {
        "type": BooleanInputDefinition,
        "description": "Specify that ALL DWIs have been acquired with opposing phase-encoding",  # noqa: E501
    },
    "rpe_header": {
        "type": BooleanInputDefinition,
        "description": "Specify that the phase-encoding information can be found in the image header(s), and that this is the information that the script should use",  # noqa: E501
    },
    "grad": {
        "type": StringInputDefinition,
        "description": "Provide the diffusion gradient table in MRtrix format",
    },
    "fslgrad": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "description": "Provide the diffusion gradient table in FSL bvecs/bvals format",
    },
    "export_grad_mrtrix": {
        "type": StringInputDefinition,
        "description": "Export the final gradient table in MRtrix format",
        "is_output_path": True,
    },
    "export_grad_fsl": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "description": "Export the final gradient table in FSL bvecs/bvals format",  # noqa: E501
    },
    "nocleanup": {
        "type": BooleanInputDefinition,
        "description": "do not delete intermediate files during script execution, and do not delete scratch directory at script completion.",  # noqa: E501
    },
    "scratch": {
        "type": StringInputDefinition,
        "description": "manually specify the path in which to generate the scratch directory.",  # noqa: E501
        "is_output_path": True,
    },
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",  # noqa: E501
    },
}

#: *DwiFslPreproc* output specification dictionary.
DWIFSLPREPROC_OUTPUT_SPECIFICATION = {
    "preprocessed_dwi": {
        "type": FileOutputDefinition,
        "description": "The output preprocessed DWI.",
    },
    "out_movement_rms": {
        "type": FileOutputDefinition,
        "description": "Summary of the ‘total movement’ in each volume",
    },
    "eddy_mask": {
        "type": FileOutputDefinition,
        "description": "Brain mask used durring eddy currents correction.",
    },
    "out_outlier_map": {
        "type": FileOutputDefinition,
        "description": "Matrix where rows represent volumes and columns represent slices. “0” indicates that scan-slice is not an outlier and “1” indicates that it is.",  # noqa: E501
    },
    "out_outlier_n_sqr_stdev_map": {
        "type": FileOutputDefinition,
        "description": "Matrix where rows represent volumes and columns represent slices. Values indicate number of standard deivations off the square root of the mean squared difference between observation and prediction is.",  # noqa: E501
    },
    "out_outlier_n_stdev_map": {
        "type": FileOutputDefinition,
        "description": "Matrix where rows represent volumes and columns represent slices. Values indicate number of standard deviations off the mean difference between observation and prediction is.",  # noqa: E501
    },
    "out_outlier_report": {
        "type": FileOutputDefinition,
        "description": "Text file with a plain language report on what outlier slices eddy has found.",  # noqa: E501
    },
    "out_parameter": {
        "type": FileOutputDefinition,
        "description": "Text file with parameters defining the field and movement for each scan.",  # noqa: E501
    },
    "out_restricted_movement_rms": {
        "type": FileOutputDefinition,
        "description": "Summary of the ‘total movement’ in each volume disregarding translation in the PE direction.",  # noqa: E501
    },
    "out_shell_alignment_parameters": {
        "type": FileOutputDefinition,
        "description": "Text file containing rigid body movement parameters between the different shells as estimated by a post-hoc mutual information based registration.",  # noqa: E501
    },
    "out_shell_pe_translation_parameters": {
        "type": FileOutputDefinition,
        "description": "Text file containing translation along the PE-direction between the different shells as estimated by a post-hoc mutual information based registration.",  # noqa: E501
    },
}
