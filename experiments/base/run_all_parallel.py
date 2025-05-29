# File: experiments/base/run_all_parallel.py

import subprocess
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

PLANNER_SCRIPTS = [
    "run_all_downward.py",
    "run_all_lpg.py",
    "run_all_mercury.py",
    "run_all_madagascar.py",
    "run_all_lapkt.py"
]

def run_script(script_name):
    log_file = Path(script_name).with_suffix('.log')
    print(f"▶ Starte {script_name} ... (Log: {log_file})")

    try:
        result = subprocess.run(
            ["python3", script_name],
            cwd=Path(__file__).parent,  # Führt die Skripte im aktuellen Ordner aus
            capture_output=True,
            text=True,
            timeout=3600  # 1 Stunde max
        )

        with open(log_file, "w") as f:
            f.write(result.stdout)
            if result.stderr:
                f.write("\n[stderr]\n")
                f.write(result.stderr)

        print(f"✅ Beendet {script_name} mit Code {result.returncode}")
        return result.returncode

    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout bei {script_name}")
        return -1
    except Exception as e:
        print(f"❌ Fehler bei {script_name}: {e}")
        return -1

if __name__ == "__main__":
    # Anzahl paralleler Prozesse anpassen, z. B. 3–4 für c2-standard-8
    with ProcessPoolExecutor(max_workers=3) as executor:
        executor.map(run_script, PLANNER_SCRIPTS)