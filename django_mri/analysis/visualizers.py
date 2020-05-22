import subprocess

from django_analyses.models.run import Run
from django_mri.models.inputs.nifti_input import NiftiInput
from django_mri.models.nifti import NIfTI
from django_mri.models.outputs.nifti_output import NiftiOutput

COMMAND = 'fsleyes --scene lightbox --worldLoc 0.8857347727542049 -7.7526201473787495 15.74170873943467 --displaySpace world --zaxis 2 --sliceSpacing 0.9999989867210388 --zrange -0.4999994933605194 132.46744991580044 --ncols 4 --nrows 1 --bgColour 0.0 0.0 0.0 --fgColour 1.0 1.0 1.0 --cursorColour 0.0 1.0 0.0 --colourBarLocation top --colourBarLabelSide top-left --colourBarSize 100.0 --labelSize 12 --performance 3 --movieSync {run_path}/T1_orig.nii.gz --name "T1_orig" --overlayType volume --alpha 100.0 --brightness 50.0 --contrast 50.0 --cmap greyscale --negativeCmap greyscale --displayRange 0.0 1692.0 --clippingRange 0.0 1708.92 --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0 {run_path}/T1_fast_pve_0.nii.gz --name "T1_fast_pve_0" --overlayType volume --alpha 100.0 --brightness 50.0 --contrast 50.0 --cmap green --negativeCmap greyscale --displayRange 0.0 1.0 --clippingRange 0.0 1.01 --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0 {run_path}/T1_fast_pve_1.nii.gz --name "T1_fast_pve_1" --overlayType volume --alpha 100.0 --brightness 50.0 --contrast 50.0 --cmap red-yellow --negativeCmap greyscale --displayRange 0.0 1.0 --clippingRange 0.0 1.01 --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0 {run_path}/T1_fast_pve_2.nii.gz --name "T1_fast_pve_2" --overlayType volume --alpha 100.0 --brightness 50.0 --contrast 50.0 --cmap blue-lightblue --negativeCmap greyscale --displayRange 0.0 1.0 --clippingRange 0.0 1.01 --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0 {run_path}/T1_fast_pveseg.nii.gz --name "T1_fast_pveseg" --disabled --overlayType volume --alpha 100.0 --brightness 50.0 --contrast 50.0 --cmap greyscale --negativeCmap greyscale --displayRange 0.0 3.0 --clippingRange 0.0 3.03 --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0 {run_path}/T1_biascorr.nii.gz --name "T1_biascorr" --disabled --overlayType volume --alpha 100.0 --brightness 50.0 --contrast 50.0 --cmap greyscale --negativeCmap greyscale --displayRange 0.0 1813.2049560546875 --clippingRange 0.0 1831.3370056152344 --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0 {run_path}/T1_biascorr_bet_skull.nii.gz --name "T1_biascorr_bet_skull" --disabled --overlayType volume --alpha 100.0 --brightness 50.0 --contrast 50.0 --cmap greyscale --negativeCmap greyscale --displayRange 0.0 100.0 --clippingRange 0.0 101.0 --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0 {run_path}/T1_biascorr_brain.nii.gz --name "T1_biascorr_brain" --disabled --overlayType volume --alpha 100.0 --brightness 50.0 --contrast 50.0 --cmap greyscale --negativeCmap greyscale --displayRange 0.0 920.9035034179688 --clippingRange 0.0 930.1125384521484 --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0 /usr/local/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz --name "MNI152_T1_1mm_brain" --disabled --overlayType volume --alpha 100.0 --brightness 50.0 --contrast 50.0 --cmap greyscale --negativeCmap greyscale --displayRange 0.0 8364.0 --clippingRange 0.0 8447.64 --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0 {run_path}/T1_subcort_seg.nii.gz --name "T1_subcort_seg" --disabled --overlayType volume --alpha 100.0 --brightness 50.0 --contrast 50.0 --cmap greyscale --negativeCmap greyscale --displayRange 0.0 58.0 --clippingRange 0.0 58.58 --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0 {run_path}/T1_to_MNI_lin.nii.gz --name "T1_to_MNI_lin" --disabled --overlayType volume --alpha 100.0 --brightness 50.0 --contrast 50.0 --cmap greyscale --negativeCmap greyscale --displayRange 0.0 1286.9368896484375 --clippingRange 0.0 1299.8062585449218 --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0 {run_path}/T1_to_MNI_nonlin.nii.gz --name "T1_to_MNI_nonlin" --disabled --overlayType volume --alpha 100.0 --brightness 50.000000684392745 --contrast 50.00000136878548 --cmap greyscale --negativeCmap greyscale --displayRange -42.08723449707031 1630.0654296875 --clippingRange -42.08723449707031 1646.7869567871094 --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0'


class FslAnatVisualizer:
    def __init__(self, run: Run):
        self.run = run

    def visualize(self) -> None:
        command = COMMAND.format(run_path=self.run.path).split(" ")
        proc = subprocess.run(command)
        return proc

    @property
    def input_image(self) -> NIfTI:
        nifti_inputs = self.run.input_set.select_subclasses(NiftiInput)
        return [inpt.value for inpt in nifti_inputs if inpt.key == "image"][0]

    @property
    def output_images(self) -> list:
        nifti_outputs = self.run.output_set.select_subclasses(NiftiOutput)
        return [output.value for output in nifti_outputs]