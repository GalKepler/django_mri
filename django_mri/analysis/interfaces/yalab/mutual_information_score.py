"""
Definition of the :class:`MutualInformationScore` class.
"""
from itertools import combinations
from pathlib import Path
from typing import Iterable, Union

import nibabel as nib
import numpy as np
import pandas as pd

# from dask.dataframe import from_pandas
from django.db.models import QuerySet
from django_mri.analysis.interfaces.yalab import messages
from django_mri.analysis.interfaces.yalab.utils import (
    get_cat12_segmentation_node,
)
from sklearn.metrics import mutual_info_score

SECONDS_IN_DAY = 60 * 60 * 24


class MutualInformationScore:
    """
    Calculates the mutual information score of the contingency matrix for each
    combination of the 2D histograms generated by CAT12 segmentation outputs.
    """

    NIFTI_SUFFIXES = [".nii"], [".nii", ".gz"]
    INFO_COLUMNS = [
        "Subject 1",
        "Subject 2",
        "Same Subject",
        "Session 1",
        "Session 2",
        "Same Session",
        "Scan 1",
        "Scan 2",
        "Scan Description 1",
        "Scan Description 2",
        "Scan Time 1",
        "Scan Time 2",
        "Time Delta",
    ]
    COMPARED_OUTPUTS = (
        # "native_grey_matter",
        # "native_white_matter",
        # "native_pve",
        "modulated_grey_matter",
        "modulated_white_matter",
        "warped_image",
        # "jacobian_determinant",
    )

    def __init__(self, bins: int = 10):
        self.bins = bins

    @staticmethod
    def _fix_output_name(output_name: str) -> str:
        return output_name.replace("_", " ").capitalize().replace("Pve", "PVE")

    @staticmethod
    def _read_nifti(path: Path) -> np.ndarray:
        data = np.asarray(nib.load(str(path)).dataobj)
        return np.nan_to_num(data.flatten())

    @staticmethod
    def _query_scan(run):
        from django_mri.models.scan import Scan

        return Scan.objects.get(_nifti__path=run.get_input("path"))

    @staticmethod
    def _calculate_days_delta(scan_1, scan_2) -> int:
        seconds_delta = np.abs((scan_1.time - scan_2.time).total_seconds())
        return int(seconds_delta / SECONDS_IN_DAY)

    @classmethod
    def _get_column_names(cls) -> list:
        return cls.INFO_COLUMNS + [
            cls._fix_output_name(output) for output in cls.COMPARED_OUTPUTS
        ]

    @classmethod
    def _read_data(cls, path: Union[Path, Iterable[Path]]) -> np.ndarray:
        if isinstance(path, (str, Path)):
            is_nifti = Path(path).suffixes in cls.NIFTI_SUFFIXES
            if is_nifti:
                return cls._read_nifti(path)
            raise ValueError(messages.NOT_NIFTI)
        elif isinstance(path, Iterable):
            return np.stack([cls._read_data(p) for p in path], axis=0)

    def _calculate_mi(self, data_1: np.ndarray, data_2: np.ndarray) -> float:
        try:
            histogram = np.histogram2d(data_1, data_2, self.bins)[0]
        except ValueError:
            pass
        else:
            return mutual_info_score(None, None, contingency=histogram)

    def run(self, runs: QuerySet = None) -> pd.DataFrame:
        node = get_cat12_segmentation_node()
        runs = runs or node.run_set.filter(status="SUCCESS")
        indices = pd.MultiIndex.from_tuples(
            combinations(range(runs.count()), 2)
        )
        scores = pd.DataFrame(index=indices, columns=self.column_names)
        # scores = from_pandas(scores, chunksize=25000)
        for i_output, output in enumerate(self.COMPARED_OUTPUTS):
            output_name = self._fix_output_name(output)
            print(output_name)
            previous_index_1 = previous_index_2 = None
            data_1 = data_2 = None
            for index, *_ in scores.itertuples():
                index_1, index_2 = index
                run_1, run_2 = runs[index_1], runs[index_2]
                if previous_index_1 != index_1:
                    path_1 = run_1.get_output(output)
                    data_1 = self._read_data(path_1)
                if previous_index_2 != index_2:
                    path_2 = run_2.get_output(output)
                    data_2 = self._read_data(path_2)
                score = self._calculate_mi(data_1, data_2)
                scores.loc[index, output_name] = score
                previous_index_1 = index_1
                previous_index_2 = index_2
                if i_output == 0:
                    scan_1 = self._query_scan(run_1)
                    scan_2 = self._query_scan(run_2)
                    session_1 = scan_1.session
                    session_2 = scan_2.session
                    subject_1 = session_1.subject
                    subject_2 = session_2.subject
                    same_subject = subject_1 == subject_2
                    scores.loc[index, "Subject 1"] = subject_1.id
                    scores.loc[index, "Subject 2"] = subject_2.id
                    scores.loc[index, "Same Subject"] = same_subject
                    scores.loc[index, "Session 1"] = session_1.id
                    scores.loc[index, "Session 2"] = session_2.id
                    if same_subject:
                        same_session = session_1 == session_2
                        scores.loc[index, "Same Session"] = same_session
                    scores.loc[index, "Scan 1"] = scan_1.id
                    scores.loc[index, "Scan 2"] = scan_2.id
                    scores.loc[
                        index, "Scan Description 1"
                    ] = scan_1.description
                    scores.loc[
                        index, "Scan Description 2"
                    ] = scan_2.description
                    scores.loc[index, "Scan Time 1"] = scan_1.time
                    scores.loc[index, "Scan Time 2"] = scan_2.time
                    if same_subject:
                        delta = self._calculate_days_delta(scan_1, scan_2)
                        scores.loc[index, "Time Delta"] = delta
        return scores

    @property
    def column_names(self) -> list:
        return self._get_column_names()