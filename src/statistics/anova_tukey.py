"""
One-Way ANOVA and Tukey HSD post-hoc statistical analysis across Sentinel-2 spectral bands.
Reference: Monterrubio-Martínez et al., Ecological Informatics 85 (2025) 102961.
Section 2.2 & 3.1, Figure 4.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from typing import Dict, Tuple, List, Optional
from pathlib import Path

from src.config import (
    SPECTRAL_BANDS,
    BAND_NAMES,
    SPECIES_NAMES,
    SPECIES_COLORS,
    RESULTS_STATS_DIR,
    RESULTS_FIGURES_DIR,
)


def run_one_way_anova(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute One-Way ANOVA for each of the 10 Sentinel-2 bands across the three mangrove species.
    Null hypothesis: Mean reflectance is identical across species for the given band.
    Alternative: At least one species has a significantly different mean reflectance.
    """
    results = []
    species_list = ["Rhizophora_mangle", "Avicennia_germinans", "Laguncularia_racemosa"]
    
    for band in SPECTRAL_BANDS:
        groups = [df[df["Spp"] == spp][band].values for spp in species_list]
        f_stat, p_val = stats.f_oneway(*groups)
        
        # Calculate group means and standard deviations
        means = {f"{spp}_mean": df[df["Spp"] == spp][band].mean() for spp in species_list}
        stds = {f"{spp}_std": df[df["Spp"] == spp][band].std() for spp in species_list}
        
        res_dict = {
            "Band": band,
            "Band_Name": BAND_NAMES[band],
            "F_Statistic": f_stat,
            "p_value": p_val,
            "Significant (p < 0.05)": p_val < 0.05,
        }
        res_dict.update(means)
        res_dict.update(stds)
        results.append(res_dict)
        
    anova_df = pd.DataFrame(results)
    return anova_df


def run_tukey_hsd(df: pd.DataFrame, alpha: float = 0.05) -> pd.DataFrame:
    """
    Perform Tukey's Honestly Significant Difference (HSD) post-hoc test
    for all 10 bands with confidence interval 95% (alpha = 0.05).
    """
    all_tukey_results = []
    
    for band in SPECTRAL_BANDS:
        tukey = pairwise_tukeyhsd(endog=df[band], groups=df["Spp"], alpha=alpha)
        # Extract summary table
        table_data = tukey.summary().data
        headers = table_data[0]
        rows = table_data[1:]
        
        for row in rows:
            row_dict = {
                "Band": band,
                "Band_Name": BAND_NAMES[band],
                "Group1": str(row[0]).strip(),
                "Group2": str(row[1]).strip(),
                "Mean_Diff": float(row[2]),
                "p_adj": float(row[3]),
                "Lower_CI_95": float(row[4]),
                "Upper_CI_95": float(row[5]),
                "Reject_H0": bool(row[6]),
            }
            all_tukey_results.append(row_dict)
            
    tukey_df = pd.DataFrame(all_tukey_results)
    return tukey_df


def plot_species_boxplots(df: pd.DataFrame, save_path: Optional[Path] = None) -> plt.Figure:
    """
    Generate publication-quality boxplots reproducing Figure 4 of the research paper:
    Boxplots for each of the species (R. mangle, A. germinans, L. racemosa) across all 10 bands.
    """
    species_order = ["Rhizophora_mangle", "Avicennia_germinans", "Laguncularia_racemosa"]
    species_labels = ["R. mangle", "A. germinans", "L. racemosa"]
    palette = [SPECIES_COLORS[s] for s in species_order]
    
    fig, axes = plt.subplots(2, 5, figsize=(18, 8), sharey=False)
    axes = axes.flatten()
    
    for idx, band in enumerate(SPECTRAL_BANDS):
        ax = axes[idx]
        sns.boxplot(
            data=df,
            x="Spp",
            y=band,
            order=species_order,
            palette=palette,
            ax=ax,
            fliersize=1,
            linewidth=1.2,
        )
        ax.set_title(f"{band} ({BAND_NAMES[band]})", fontsize=11, fontweight="bold")
        ax.set_xlabel("")
        ax.set_ylabel("Surface Reflectance" if idx % 5 == 0 else "")
        ax.set_xticklabels(species_labels, fontsize=9, rotation=15)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        
    plt.suptitle(
        "Reproduced Figure 4: Reflectance Boxplots by Species across 10 Sentinel-2 Bands\n"
        "(All bands exhibit statistically significant difference, p < 0.05)",
        fontsize=13,
        fontweight="bold",
        y=0.98
    )
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        
    return fig
