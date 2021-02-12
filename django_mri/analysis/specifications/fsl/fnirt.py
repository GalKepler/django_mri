"""
Input and output specification dictionaries for FSL's FNIRT_ script.

.. _FNIRT:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FNIRT
"""

from django_analyses.models.input.definitions import (BooleanInputDefinition,
                                                      FileInputDefinition,
                                                      FloatInputDefinition,
                                                      IntegerInputDefinition,
                                                      ListInputDefinition,
                                                      StringInputDefinition)
from django_analyses.models.output.definitions import FileOutputDefinition
from django_mri.models.inputs.nifti_input_definition import \
    NiftiInputDefinition
from django_mri.models.outputs.nifti_output_definition import \
    NiftiOutputDefinition

#: *FNIRT* input specification dictionary.
FNIRT_INPUT_SPECIFICATION = {
    "in_file": {
        "type": FileInputDefinition,
        "required": True,
        "description": "A NIfTI format file to register to the reference.",
        "is_configuration": False,
    },
    "ref_file": {
        "type": FileInputDefinition,
        "required": True,
        "description": "A NIfTI format file to register the input file with.",
    },
    "affine_file": {
        "type": FileInputDefinition,
        "description": "File containing an existing affine transformation matrix.",  # noqa: E501
    },
    "inwarp_file": {
        "type": FileInputDefinition,
        "description": "File containing initial non-linear warps.",
    },
    "in_intensitymap_file": {
        "type": FileInputDefinition,
        "description": "File containing initial initial intensity mapping usually generated by a previous FNIRT run.",  # noqa: E501
    },
    "fieldcoeff_file": {
        "type": StringInputDefinition,
        "description": "Name for field coefficients file to output.",
        "is_output_path": True,
        "default": "field_coefficients.nii.gz",
    },
    "warped_file": {
        "type": StringInputDefinition,
        "description": "Path for the output image.",
        "is_output_path": True,
        "default": "warped.nii.gz",
    },
    "field_file": {
        "type": StringInputDefinition,
        "description": "Path for the output file with field.",
        "is_output_path": True,
        "default": "field.nii.gz",
    },
    "jacobian_file": {
        "type": StringInputDefinition,
        "description": "Path to the output file for writing out the Jacobian of the field (for diagnostic or VBM purposes).",  # noqa: E501
        "is_output_path": True,
        "default": "jacobian.nii.gz",
    },
    "modulatedref_file": {
        "type": StringInputDefinition,
        "description": "Path to the output file for writing out intensity modulated --ref (for diagnostic purposes).",  # noqa: E501
        "is_output_path": True,
        "default": "modulatedref.nii.gz",
    },
    # This returns a list with one .txt and one .nii.gz files.
    # It needs to either have a wrapper or a special configuration
    # made for this conditions.
    # "out_intensitymap_file": {
    #     "type": StringInputDefinition,
    #     "description": "Path to the output file for writing information pertaining to intensity mapping.", # noqa: E501
    #     "is_output_path": True,
    #     "default": "out_intensitymap",
    # },
    "log_file": {
        "type": StringInputDefinition,
        "description": "Path for a log file.",
        "is_output_path": True,
        "default": "log.txt",
    },
    "config_file": {
        "type": FileInputDefinition,
        "description": "Path for a config file specifying command line arguments.",  # noqa: E501
        "required": False,
    },
    "refmask_file": {
        "type": FileInputDefinition,
        "description": "Path for a file with a mask in the reference space.",
        "required": False,
    },
    "inmask_file": {
        "type": FileInputDefinition,
        "description": "Path for a file with a mask in the input image space.",
        "required": False,
    },
    "skip_refmask": {
        "type": BooleanInputDefinition,
        "description": "Skip specified refmask_file if set.",
        "required": False,
    },
    "skip_inmask": {
        "type": BooleanInputDefinition,
        "description": "Skip specified inmask_file if set.",
        "required": False,
    },
    "apply_refmask": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "A list of iterations to use the reference mask on (1 to use, 0 to skip).",  # noqa: E501
        "required": False,
    },
    "apply_inmask": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "A list of iterations to use the input mask on (1 to use, 0 to skip).",  # noqa: E501
        "required": False,
    },
    "skip_implicit_ref_masking": {
        "type": BooleanInputDefinition,
        "description": "Skip implicit masking based on value in reference image.",  # noqa: E501
        "required": False,
    },
    "skip_implicit_in_masking": {
        "type": BooleanInputDefinition,
        "description": "Skip implicit masking based on value in input image.",
        "required": False,
    },
    "refmask_val": {
        "type": FloatInputDefinition,
        "description": "Value to mask out in reference image.",
        "default": 0,
        "required": False,
    },
    "inmask_val": {
        "type": FloatInputDefinition,
        "description": "Value to mask out in input image.",
        "default": 0,
        "required": False,
    },
    "max_nonlin_iter": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "List containing the maximal numbers of non-linear iterations.",  # noqa: E501
        "default": [5, 5, 5, 5],
        "required": False,
    },
    "subsampling_scheme": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "Sub-sampling scheme.",
        "default": [4, 2, 1, 1],
        "required": False,
    },
    "warp_resolution": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "Approximate resolution (in mm) of warp basis in the X, Y, and Z axes.",  # noqa: E501
        "default": [10, 10, 10],
        "min_length": 3,
        "max_length": 3,
        "required": False,
        "as_tuple": True,
    },
    "spline_order": {
        "type": IntegerInputDefinition,
        "description": "Order of spline (2 = quadratic, 3 = cubic).",
        "default": 3,
        "required": False,
    },
    "in_fwhm": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "FWHM (in mm) of gaussian smoothing kernel for the input volume.",  # noqa: E501
        "default": [6, 4, 2, 2],
        "required": False,
    },
    "ref_fwhm": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "FWHM (in mm) of gaussian smoothing kernel for the reference volume.",  # noqa: E501
        "default": [4, 2, 0, 0],
        "required": False,
    },
    "regularization_model": {
        "type": StringInputDefinition,
        "description": "Model for regularisation of warp-field.",
        "choices": ["membrane_energy", "bending_energy"],
        "default": "bending_energy",
        "required": False,
    },
    "regularization_lambda": {
        "type": ListInputDefinition,
        "element_type": "FLT",
        "description": "Weight of regularisation.",
        "required": False,
    },
    "skip_lambda_ssq": {
        "type": BooleanInputDefinition,
        "description": "If true, lambda is not weighted by current ssq.",
        "default": False,
        "required": False,
    },
    "jacobian_range": {
        "type": ListInputDefinition,
        "element_type": "FLT",
        "description": "Allowed range of Jacobian determinants.",
        "default": [0.01, 100.0],
        "required": False,
        "as_tuple": True,
    },
    "derive_from_ref": {
        "type": BooleanInputDefinition,
        "description": "If true, reference image is used to calculate derivatives.",  # noqa: E501
        "default": False,
        "required": False,
    },
    "intensity_mapping_model": {
        "type": StringInputDefinition,
        "description": "Model for intensity-mapping.",
        "choices": [
            "none",
            "global_linear",
            "global_non_linear",
            "local_linear",
            "global_non_linear_with_bias",
            "local_non_linear",
        ],
        "required": False,
    },
    "intensity_mapping_order": {
        "type": IntegerInputDefinition,
        "description": "Order of poynomial for mapping intensities.",
        "default": 5,
        "required": False,
    },
    "biasfield_resolution": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "Approximate resolution (in mm) of warp basis in the X, Y, and Z axes.",  # noqa: E501
        "default": [50, 50, 50],
        "min_length": 3,
        "max_length": 3,
        "as_tuple": True,
        "required": False,
    },
    "bias_regularization_lambda": {
        "type": FloatInputDefinition,
        "description": "Weight of regularisation for bias-field.",
        "default": 10000,
        "required": False,
    },
    "skip_intensity_mapping": {
        "type": BooleanInputDefinition,
        "description": "Whether to skip estimate intensity-mapping.",
        "default": False,
        "required": False,
    },
    "apply_intensity_mapping": {
        "type": ListInputDefinition,
        "element_type": "INT",
        "description": "List of subsampling levels to apply intensity mapping for (0 to skip, 1 to apply).",  # noqa: E501
        "required": False,
    },
    "hessian_precision": {
        "type": StringInputDefinition,
        "description": "Precision for representing Hessian.",
        "choices": ["double", "float"],
        "default": "double",
        "required": False,
    },
    "output_type": {
        "type": StringInputDefinition,
        "description": "Output file format.",
        "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
        "required": False,
    },
}

#: *FNIRT* output specification dictionary.
FNIRT_OUTPUT_SPECIFICATION = {
    "fieldcoeff_file": {
        "type": FileOutputDefinition,
        "description": "Field coefficients.",
    },
    "warped_file": {"type": NiftiOutputDefinition, "description": "Warped image.",},
    "field_file": {"type": NiftiOutputDefinition, "description": "Warp field.",},
    "jacobian_file": {
        "type": NiftiOutputDefinition,
        "description": "Jacobian of the field.",
    },
    "modulatedref_file": {
        "type": NiftiOutputDefinition,
        "description": "Intensity modulated reference.",
    },
    # "out_intensitymap_file": {
    #     "type": FileOutputDefinition,
    #     "description": "Intensity mapping information.",
    # },
    "log_file": {"type": FileOutputDefinition, "description": "Run log."},
}
