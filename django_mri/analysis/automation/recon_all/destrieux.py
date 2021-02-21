import matplotlib.pyplot as plt
import pandas as pd
from nilearn import datasets, plotting
from sklearn.preprocessing import StandardScaler

# Nilearn Destrieux region name with no represenation in FreeSurfer
MEDIAL_WALL = "Medial_wall"


def parse_destrieux_label(label: bytes) -> str:
    return label.decode().replace("_and_", "&")


def plot_destrieux_surface(
    stats_df: pd.DataFrame,
    hemisphere: str = "Left",
    measurement: str = "Surface Area",
    average: bool = False,
    std: bool = False,
    standardize: bool = False,
    title: str = None,
    symmetric_cmap: bool = False,
    cmap: str = None,
    vmin: float = None,
    factor: int = 1,
) -> plt.Figure:
    title = title or f"{measurement} ({hemisphere})"
    destrieux_atlas = datasets.fetch_atlas_surf_destrieux()
    destrieux_labels = [
        parse_destrieux_label(label) for label in destrieux_atlas["labels"][1:]
    ]
    fsaverage = datasets.fetch_surf_fsaverage()
    data = stats_df.xs("Destrieux", level="Atlas").copy()
    if average:
        data = data.mean(level=["Hemisphere", "Region Name"])
        title = f"Average {title}"
    if std:
        data = data.std(level=["Hemisphere", "Region Name"])
        title = f"{measurement} Standard Deviation ({hemisphere})"
        vmin = 0
    if standardize:
        data.loc[:, :] = StandardScaler().fit_transform(data)
        title = f"Standardized {title}"
        symmetric_cmap = True
        cmap = cmap if cmap is not None else "coolwarm"
    cmap = cmap if cmap is not None else "Reds"
    hemi_stats = data.xs(hemisphere, level="Hemisphere")
    destrieux_projection = destrieux_atlas[f"map_{hemisphere.lower()}"].copy()
    region_ids = sorted(set(destrieux_projection))
    for i, region_id in enumerate(region_ids):
        label = destrieux_labels[i]
        if label == MEDIAL_WALL:
            value = 0
        else:
            value = hemi_stats.loc[label, measurement] * factor
        destrieux_projection[destrieux_projection == region_id] = value
    surface = plotting.view_surf(
        fsaverage[f"infl_{hemisphere.lower()}"],
        destrieux_projection,
        bg_map=fsaverage[f"sulc_{hemisphere.lower()}"],
        cmap=cmap,
        title=title,
        symmetric_cmap=symmetric_cmap,
        vmin=vmin,
    )
    surface.resize(900, 600)
    return surface
