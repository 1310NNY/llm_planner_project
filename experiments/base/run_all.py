import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PLANNER_SCRIPTS = [
    "run_all_siw.py",
    "run_all_bfs_f.py",
    "run_all_mercury.py",
    "run_all_madagascar.py",
    "run_all_fd.py",
]

def run_script(script_name):
    log_file = Path(script_name).with_suffix('.log')
    print(f"▶ Starte {script_name} ... (Log: {log_file})")

    try:
        with open(log_file, "w") as f:
            process = subprocess.Popen(
                ["python3", script_name],
                cwd=Path(__file__).parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Zeilen zählen für punktuelle Fortschrittsanzeige
            line_counter = 0
            for line in process.stdout:
                f.write(line)
                line_counter += 1
                if line_counter % 10 == 0:
                    print(f"[{script_name}] ... läuft ({line_counter} Zeilen)")

        return_code = process.wait()
        print(f"✅ Beendet {script_name} mit Code {return_code}")
        return return_code

    except Exception as e:
        print(f"❌ Fehler bei {script_name}: {e}")
        return -1

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(run_script, PLANNER_SCRIPTS)
