
# MD Project Setup Tool

This tool helps you **quickly initialize a molecular dynamics (MD) project** with a standardized folder structure and naming conventions for both **protein-only** and **protein–membrane** simulations.

```
pip install start-md-project
start-md-project name_of_project
```

It supports the following force fields:

- **CHARMM36m**
- **Martini 2.2**
- **Martini 3**

If desired, the tool can automatically download the appropriate **MDP files**, **`toppar/` folders**, and **`.itp` files** for the selected force field from this GitHub.

---

## 📁 Folder Structure

```
.
├── mdp
│   └── FF
│       ├── in_water
│       └── in_membrane
├── toppar
├── scripts
├── analysis
├── simulations
│   └── FF
│       ├── protein
│       ├── membrane
│       └── protein+membrane
└── molecules
```

### Description of Folders

- **`mdp/`**  
  Stores all `.mdp` files, organized by force field and environment (`in_water`, `in_membrane`).  
  _All simulations should reference MDP files from here._

- **`toppar/`**  
  Contains force field parameters, including `.itp` and topology-related files.  
  _All systems should include parameters exclusively from this directory._

- **`scripts/`**  
  Custom helper or automation scripts.

- **`analysis/`**  
  Placeholder for analysis scripts, tools, or result files.

- **`simulations/`**  
  Project workspace where system-specific simulations are built and run, structured by force field and system type:
  - `protein`
  - `membrane`
  - `protein+membrane`

- **`molecules/`**  
  Repository for initial molecular structures (e.g., PDB files, AlphaFold predictions, etc.).


