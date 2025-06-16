import subprocess
from pathlib import Path
import uuid

def is_valid_with_val(domain_str: str, problem_file: str) -> bool:
    try:
        problem_path = Path(problem_file).resolve()
        mount_dir = problem_path.parent
        domain_filename = f"domain_tmp_{uuid.uuid4().hex[:8]}.pddl"
        tmp_domain_path = mount_dir / domain_filename

        # 📝 Temporäre Domain speichern
        with open(tmp_domain_path, "w") as f:
            f.write(domain_str)

        # 🐳 Docker-Befehl
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-v", f"{mount_dir}:/pddl",
                "val_validator",
                f"/pddl/{domain_filename}",
                f"/pddl/{problem_path.name}"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # ✅ NEU: Exit-Code auswerten
        return result.returncode == 0

    except Exception as e:
        print("❌ VAL-Check fehlgeschlagen:", e)
        return False

    finally:
        try:
            tmp_domain_path.unlink()
        except Exception:
            pass
