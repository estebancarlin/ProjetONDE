# Wound Healing Simulation — Optics/Photonics Project (Ecole Centrale Marseille)

## Context

This project was developed within the course **ONDES (Waves)** at **Ecole Centrale Marseille**, as part of a semester-long group assignment. The aim was to explore a physical phenomenon or application related to optics or photonics.

Our group chose to model the **healing dynamics of a wound on skin tissue**, simulating how a wound transitions through various healing phases — from intact skin to wound, healing, and healed states — and optionally including a *laser stimulation effect* to regenerate healed skin back into intact skin.

---

## Project Description

### Biological Modeling

The simulation represents a 2D square matrix corresponding to skin tissue. Each cell of the matrix can exist in one of four states:

| State Code | Meaning            | Color (Visual Output)  |
|------------|--------------------|------------------------|
| `-1`       | Intact Skin        | Navajo White           |
| `0`        | Wounded Skin       | Tomato Red             |
| `1`        | Healing Skin       | Light Salmon           |
| `2`        | Healed Skin        | Antique White          |

The wound is modeled as a central square region where skin is damaged. Over several iterations (timesteps), healing progresses depending on local neighborhood conditions and random probabilities. The process can be optionally influenced by a “laser effect,” which regenerates healed cells back to the intact state.

---

## Repository Structure

This repository contains two versions of the simulation code:

### 1. `CodeProjetONDES.py` (Original : 2022)

- Written during the project.
- Fully functional, but includes:
  - French comments and variable names.
  - Mixed coding styles and redundant imports.
  - Hardcoded paths for image saving.
- Maintained for academic transparency.

### 2. `ProjectWAVES_cleaned.py` (Cleaned Version : 2025)

- Refactored for clarity and repository-readiness.
- Features:
  - English variable names and comments.
  - Modularized and well-documented functions.
  - Removed unused imports and cleaned code style (PEP8 compliant).
  - Optional visualization/image saving using `matplotlib`.
  - Suitable for further research and academic extension.

---

##  Example Simulation

To run a basic simulation with image export:

```python
python ProjectWAVES_cleaned.py
