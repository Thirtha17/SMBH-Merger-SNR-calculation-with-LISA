# SMBH Merger SNR Calculation with LISA

This repository contains notebook-based analyses for estimating signal-to-noise ratios (SNRs) of supermassive black hole (SMBH) merger populations in the LISA detector. The work uses merger catalogs from IllustrisTNG simulations, cached NumPy arrays, and LISA waveform/sensitivity tools to explore binary black hole and EMRI-like signal calculations.

## Repository Contents

- `SMBH Merger Analysis for Cosmological Simulations TNG-300.ipynb` - main analysis notebook for the TNG-300 merger catalog.
- `SMBH Merger Analysis for Cosmological Simulations TNG-50.ipynb` - corresponding analysis notebook for the TNG-50 catalog.
- `Mass_Distribution.ipynb` - mass and SNR distribution analysis/plots.
- `Jilians.ipynb` - analysis using the Jillian data inputs.
- `EmriWaveForm.ipynb` - EMRI waveform exploration.
- `bbhx_tutorial.ipynb` and `test.ipynb` - BBHx/LISA waveform experiments and tutorial work.
- `emri_utils.py` - helper functions for EMRI waveform generation, plotting, merger-time adjustment, and SNR calculation.
- `blackhole_mergers.hdf5` and `blackhole_mergers_tng300.hdf5` - merger catalog data files.
- `*.npy` and `parameters.npz` - cached intermediate arrays and SNR results used by the notebooks.
- `*.png` - generated figures.
- `EMRIParameters.md` - notes on EMRI parameters.

## Data Files

The notebooks expect the `.hdf5`, `.npy`, and `.npz` data files to be available in the repository root. Many cells load arrays by relative filename, for example:

```python
np.load("snr_tng300.npy")
np.load("M_1_jillia.npy")
```

Keep notebook execution in the repo root unless you update the paths.

## Python Environment

The notebooks use a scientific Python stack plus LISA-specific packages. Core dependencies include:

- `numpy`
- `scipy`
- `matplotlib`
- `h5py`
- `pandas`
- `astropy`
- `lisatools` / `lisaanalysistools`
- `bbhx`
- `few`
- `eryn`

Some of the LISA packages can be sensitive to Python, NumPy, and SciPy versions. If imports fail, create a fresh environment and install the LISA packages according to their current documentation.

## Typical Workflow

1. Open the repository root in Jupyter or VS Code.
2. Start with either:
   - `SMBH Merger Analysis for Cosmological Simulations TNG-300.ipynb`
   - `SMBH Merger Analysis for Cosmological Simulations TNG-50.ipynb`
3. Run the setup/import cells.
4. Load the corresponding HDF5 catalog and cached `.npy` SNR arrays.
5. Recompute SNR arrays only when needed, since waveform calculations may be expensive.
6. Use `Mass_Distribution.ipynb` for distribution plots and comparisons.

## Notes

- This is currently a research/notebook repository, not an installable Python package.
- Cached `.npy` files are part of the analysis state. Remove or regenerate them carefully, because several notebooks load them directly.
- `emri_utils.py` imports local `.npy` files at module import time, so those files must exist before importing the module.
- `:Zone.Identifier` files are Windows metadata artifacts and are not required for the analysis.
