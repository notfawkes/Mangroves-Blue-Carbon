"""
Orchestrator to execute all Jupyter Notebooks sequentially in clean environments
and persist outputs for demonstration and CEP evaluation.
"""

import os
import sys
import time
from pathlib import Path
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

NOTEBOOKS = [
    "01_dataset_audit.ipynb",
    "02_exploratory_analysis.ipynb",
    "03_anova_tukey.ipynb",
    "04_three_class_mangrove_mlp.ipynb",
    "05_paper_models_transcription_and_analysis.ipynb",
    "06_architecture_comparison.ipynb",
    "07_spatial_validation.ipynb",
]

def execute_notebook(nb_name: str, notebooks_dir: Path) -> bool:
    nb_path = notebooks_dir / nb_name
    print(f"\n=======================================================")
    print(f"Executing: {nb_name} ...")
    print(f"=======================================================")
    
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
        
    ep = ExecutePreprocessor(timeout=900, kernel_name="python3")
    start_time = time.time()
    
    try:
        ep.preprocess(nb, {"metadata": {"path": str(notebooks_dir)}})
        elapsed = time.time() - start_time
        print(f"SUCCESS: {nb_name} executed in {elapsed:.2f} seconds.")
        
        # Save populated notebook with executed outputs
        with open(nb_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        return True
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"FAILED: {nb_name} failed after {elapsed:.2f} seconds!")
        print(f"Error: {e}")
        return False

def main():
    root = Path(__file__).resolve().parent
    notebooks_dir = root / "notebooks"
    
    # If specific notebooks are passed as CLI arguments, execute only those
    selected = sys.argv[1:] if len(sys.argv) > 1 else NOTEBOOKS
    
    print(f"Starting sequential execution of notebooks: {selected}...")
    all_passed = True
    timings = {}
    
    for nb in selected:
        t0 = time.time()
        success = execute_notebook(nb, notebooks_dir)
        timings[nb] = (success, time.time() - t0)
        if not success:
            all_passed = False
            break
            
    print("\n" + "=" * 60)
    print("NOTEBOOK EXECUTION SUMMARY:")
    print("=" * 60)
    for nb, (success, duration) in timings.items():
        status = "PASSED" if success else "FAILED"
        print(f"  {nb:<48} : {status} ({duration:.2f}s)")
        
    if all_passed:
        print("\nAll target notebooks successfully executed from top to bottom!")
        sys.exit(0)
    else:
        print("\nOne or more notebooks failed. Please inspect errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
