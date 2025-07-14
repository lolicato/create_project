import os
import shutil
import argparse
from datetime import datetime
import requests
import zipfile
from io import BytesIO

README_TEMPLATE = """# {project}

Project created with *project-creator* on {date}.

## Layout

```
.
├── mdp
│   └── {ff}
{in_water_files}{in_membrane_files}├── toppar
├── scripts
├── analysis
├── simulations
│   └── {ff}
{simulation_structure}└── molecules
```

*Add your project description here.*
"""

def list_mdp_files(path):
    if not os.path.exists(path):
        return ""
    files = [f for f in os.listdir(path) if f.endswith('.mdp')]
    return ''.join([f"│   │   └── {f}\n" for f in files]) or ""

def create_structure(base_path, ff):
    dirs = [
        f"mdp/{ff}/in_water",
        f"mdp/{ff}/in_membrane",
        "toppar",
        "scripts",
        "analysis",
        f"simulations/{ff}/protein",
        f"simulations/{ff}/membrane",
        f"simulations/{ff}/protein+membrane",
        "molecules"
    ]
    for d in dirs:
        os.makedirs(os.path.join(base_path, d), exist_ok=True)

def copy_charmm_files(src, dest, ff):
    for sub in ['in_water', 'in_membrane']:
        src_sub = os.path.join(src, 'mdp', sub)
        dest_sub = os.path.join(dest, f'mdp/{ff}', sub)
        if os.path.isdir(src_sub):
            for file in os.listdir(src_sub):
                if file.endswith('.mdp'):
                    shutil.copy(os.path.join(src_sub, file), dest_sub)

    toppar_src = os.path.join(src, 'toppar')
    toppar_dest = os.path.join(dest, 'toppar')
    if os.path.isdir(toppar_src):
        for item in os.listdir(toppar_src):
            s = os.path.join(toppar_src, item)
            d = os.path.join(toppar_dest, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy(s, d)

def download_ff_from_github(dest, ff):
    zip_url = "https://github.com/lolicato/create_project/archive/refs/heads/main.zip"
    print(f"Downloading {ff} files from GitHub...")
    response = requests.get(zip_url)
    if response.status_code != 200:
        raise RuntimeError("Failed to download from GitHub.")

    with zipfile.ZipFile(BytesIO(response.content)) as z:
        for member in z.namelist():
            # MDP files
            if f"create_project-main/mdp/{ff}/" in member:
                filename = os.path.basename(member)
                if filename:
                    rel_path = member.split(f"mdp/{ff}/")[-1]
                    if rel_path:
                        dest_path = os.path.join(dest, f"mdp/{ff}", rel_path)
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        with z.open(member) as source, open(dest_path, "wb") as target:
                            shutil.copyfileobj(source, target)
            # TOPPAR files
            elif f"create_project-main/toppar/{ff}/" in member:
                filename = os.path.basename(member)
                if filename:
                    rel_path = member.split(f"toppar/{ff}/")[-1]
                    if rel_path:
                        dest_path = os.path.join(dest, "toppar", rel_path)
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        with z.open(member) as source, open(dest_path, "wb") as target:
                            shutil.copyfileobj(source, target)
            # Scripts
            elif "create_project-main/scripts/" in member:
                filename = os.path.basename(member)
                if filename:
                    rel_path = member.split("scripts/")[-1]
                    if rel_path:
                        dest_path = os.path.join(dest, "scripts", rel_path)
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        with z.open(member) as source, open(dest_path, "wb") as target:
                            shutil.copyfileobj(source, target)

def write_readme(dest, ff):
    in_water = list_mdp_files(os.path.join(dest, f"mdp/{ff}/in_water"))
    in_membrane = list_mdp_files(os.path.join(dest, f"mdp/{ff}/in_membrane"))
    simulation_structure = "".join([
        f"│   │   └── {folder}\n" for folder in ["protein", "membrane", "protein+membrane"]
    ])
    readme_content = README_TEMPLATE.format(
        project=os.path.basename(dest),
        date=datetime.today().strftime('%Y-%m-%d'),
        ff=ff,
        in_water_files=in_water,
        in_membrane_files=in_membrane,
        simulation_structure=simulation_structure
    )
    with open(os.path.join(dest, "README.md"), 'w') as f:
        f.write(readme_content)

def main():
    parser = argparse.ArgumentParser(description="Create a biomolecular project structure.")
    parser.add_argument("name", help="Name of the project")
    parser.add_argument("--charmm", help="Path to CHARMM36m templates", default=None)
    parser.add_argument("--force", action="store_true", help="Overwrite existing folder")

    args = parser.parse_args()

    # Select forcefield (now supports multiple options)
    available_ffs = ["CHARMM36m", "MARTINI2.2", "MARTINI3"]
    print("Available force fields:")
    for i, ff in enumerate(available_ffs, 1):
        print(f"  {i}. {ff}")
    selected = input("Select a force field [1]: ") or "1"
    try:
        ff = available_ffs[int(selected)-1]
    except (ValueError, IndexError):
        print("Invalid selection. Exiting.")
        exit(1)

    project_path = os.path.abspath(args.name)

    if os.path.exists(project_path):
        if args.force:
            shutil.rmtree(project_path)
        else:
            print(f"Error: {project_path} already exists. Use --force to overwrite.")
            exit(1)

    print(f"Creating project at: {project_path} with force field {ff}")
    create_structure(project_path, ff)

    if args.charmm:
        print(f"Copying CHARMM36m files from {args.charmm}")
        copy_charmm_files(args.charmm, project_path, ff)
    else:
        choice = input(f"Download {ff} files from GitHub? [Y/n]: ").lower()
        if choice in ["", "y", "yes"]:
            download_ff_from_github(project_path, ff)

    write_readme(project_path, ff)
    print("Done.")

if __name__ == "__main__":
    main()