"""
Input and output specification dictionaries for MRtrix's *dwibiascorrect*
script.

See Also
--------
* `nipype.interfaces.mrtrix3.preprocess.DWIBiasCorrect`_

Notes
-----
For more information, see MRtrix3's `dwibiascorrect reference`_.

.. _dwibiascorrect reference:
   https://mrtrix.readthedocs.io/en/latest/reference/commands/dwibiascorrect.html
.. _nipype.interfaces.mrtrix3.preprocess.DWIBiasCorrect:
   https://nipype.readthedocs.io/en/1.4.1/api/generated/nipype.interfaces.mrtrix3.preprocess.html#dwibiascorrect
"""

from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    FileInputDefinition,
    IntegerInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition

#: *DWIBiasCorrect* input specification dictionary.
BIAS_CORRECT_INPUT_SPECIFICATION = {
    "in_file": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Input DWI image.",
        "is_configuration": False,
    },
    "use_ants": {
        "type": BooleanInputDefinition,
        "description": "Use ANTS N4 to estimate the inhomogeneity field. Mutually exclusive with inputs: use_fsl.",  # noqa: E501
    },
    "use_fsl": {
        "type": BooleanInputDefinition,
        "description": "Use FSL FAST to estimate the inhomogeneity field. Mutually exclusive with inputs: use_ants.",  # noqa: E501
    },
    "bias": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "The output noise map.",
        "default": "bias.mif",
    },
    "grad_file": {
        "type": StringInputDefinition,
        "description": "DWI gradient scheme (MRTrix format). Mutually exclusive with inputs: grad_fsl.",  # noqa: E501
    },
    "grad_fsl": {
        "type": StringInputDefinition,
        "description": "DWI gradient scheme (FSL format). Mutually exclusive with inputs: grad_file.",  # noqa: E501
    },
    "in_bval": {
        "type": StringInputDefinition,
        "description": "Bvals file in FSL format.",
    },
    "in_bvec": {
        "type": StringInputDefinition,
        "description": "Bvecs file in FSL format.",
    },
    "in_mask": {"type": FileInputDefinition, "description": "Mask image.",},
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "Number of threads. if zero, the number of available cpus will be used.",  # noqa: E501
    },
    "out_file": {
        "type": StringInputDefinition,
        "is_output_path": True,
        "description": "The output denoised DWI image.",
        "default": "bias_corrected.mif",
    },
}

#: *DWIBiasCorrect* output specification dictionary.
BIAS_CORRECT_OUTPUT_SPECIFICATION = {
    "bias": {
        "type": FileOutputDefinition,
        "description": "The output bias field.",
    },
    "out_file": {
        "type": FileOutputDefinition,
        "description": "The output denoised DWI image.",
    },
}
