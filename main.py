import json
import subprocess #-> This allows Python talk to the terminal and run commands like docker ps, qemu img etc
from pathlib import Path


# Run a terminal command and get (ok, stdout, stderr)
def run(cmd, timeout=120):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)                          
        return (p.returncode == 0), (p.stdout or "").strip(), (p.stderr or "").strip() # -> returns (ok, stdout, stderr)

    except FileNotFoundError:
        return False, "", f"Command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    
    # p.returncode (exit code)
    # p.stdout (normal output)
    # p.stderr (error output)

# --------------------
# Docker actions
# --------------------
def create_dockerfile():
    path_str = input("Dockerfile path (example: /Users/you/Desktop/Cloud-Management-System/Dockerfile or ./Dockerfile): ").strip()
    print("Type Dockerfile lines. Type EOF to finish.")

    lines = []
    while True:
        line = input()
        if line.strip() == "EOF":
            break
        lines.append(line)

    path = Path(path_str).expanduser().resolve() #-> ./Dockerfile will become: /Users/yourname/Desktop/Cloud-Management-System/Dockerfile
    path.parent.mkdir(parents=True, exist_ok=True) #-> This will create the parent folder if it does not exit, if flase, python will throw an error like "File Exists"
    path.write_text("\n".join(lines), encoding="utf-8") #-> Write dockerfile text into to file location
    print(f"✅ Saved Dockerfile to: {path}")


def build_image():
    df_path = input("Dockerfile path: ").strip()
    tag = input("Image tag (example: myapp:1.0): ").strip() #-> name:version

    df = Path(df_path).expanduser().resolve() #-> Convert String to actual path
    if not df.exists(): #-> if path does not exist
        print("❌ Dockerfile not found.") #-> print dockerfile not found
        return #-> This retrun statemetn will exit the fucntion early

    ok, out, err = run(["docker", "build", "-t", tag, "-f", str(df), str(df.parent)], timeout=900)
    if ok: #-> if true
        print("✅ Build successful.")
        if out:#-> if output is not an empty line
            print(out) #-> build the image and show image details
    else: #-> if false
        print("❌ Build failed.")
        print(err or out) #-> display the error that occured. If err is empty, then will display output


def list_images():
    ok, out, err = run(["docker", "images"])
    if ok: #-> if true
        print(out) #-> list images
    else:#-> if false
        print("❌ Failed to list images.")
        print(err) #-> will display error that occured


def list_running_containers():
    ok, out, err = run(["docker", "ps"])
    if ok: #-> if true
        print(out) #-> will display details of all running containers
    else:#-> if false
        print("❌ Failed to list running containers.")
        print(err)


def stop_container():
    cid = input("Container ID or name: ").strip()
    ok, out, err = run(["docker", "stop", cid])
    if ok: #-> if true
        print("✅ Stopped.")
        if out: #-> if output is not an empty line
            print(out) #-> we print it
    else:#-> if false
        print("❌ Stop failed.")
        print(err or out)#-> display the error that occured. If err is empty, then will display output


#What this function does
#Ask the user: “what word are you looking for?”
#Get a list of your local images
#Keep only the ones that contain that word
#Print only those

def search_local_images():
    q = input("Search local images: ").strip().lower()

    ok, out, err = run(["docker", "images"])
    if not ok:
        print("❌ Failed to list local images.")
        print(err or out)
        return

    matches = [line for line in out.splitlines() if q in line.lower()]
    print("\n".join(matches) if matches else "(no matches)")



def search_dockerhub():
    term = input("DockerHub search term: ").strip()
    ok, out, err = run(["docker", "search", term])
    if ok:#-> if true
        print(out)#-> display online images, even if never pulled
    else:#if false
        print("❌ DockerHub search failed.")
        print(err or out)#-> display the error that occured. If err is empty, then will display output


def pull_image():
    image = input("Image to pull (example: nginx:latest): ").strip()
    ok, out, err = run(["docker", "pull", image], timeout=900)
    if ok:#-> if true
        print("✅ Pull successful.")
        print(out) #-> will display desired image
    else:#-> if false
        print("❌ Pull failed.")
        print(err or out)#-> display the error that occured. If err is empty, then will display output


# --------------------
# VM actions (QEMU) -> my iso path: "C:\Users\HP\Downloads\ubuntu-20.04.6-desktop-amd64.iso"
# --------------------
def create_vm_interactive():
    ok1, _, _ = run(["qemu-img", "--version"])
    ok2, _, _ = run(["qemu-system-x86_64", "--version"])
    if not (ok1 and ok2):
        print("❌ QEMU not found. Install QEMU first.")
        return

    name = input("VM name: ").strip()
    try:
        cpu = int(input("CPU cores (example: 2): ").strip())
        mem = int(input("Memory MB (example: 2048): ").strip())
        disk_gb = int(input("Disk GB (example: 20): ").strip())
    except ValueError:
        print("❌ Please enter valid numbers.")
        return

    disk_path = input("Disk path (example: ./vm1.qcow2): ").strip()
    if cpu <= 0 or mem <= 0 or disk_gb <= 0:
        print("❌ CPU/memory/disk must be positive.")
        return

    ok, out, err = run(["qemu-img", "create", "-f", "qcow2", disk_path, f"{disk_gb}G"]) #-> create VM qcow2 disk image
    if not ok:
        print("❌ Disk creation failed.")
        print(err or out)
        return

    # ISO attach
    iso_path = input("Ubuntu ISO path (press Enter to skip): ").strip()
    iso_path = iso_path.strip().strip('"').strip("'")

    cmd = ["qemu-system-x86_64", "-m", str(mem), "-smp", str(cpu), "-hda", disk_path] # -> qemu-system-x86_64 -m 2048 -smp 2 -hda ./vm1.qcow2

    # If ISO provided, boot from it installer
    if iso_path:
        iso = Path(iso_path).expanduser().resolve() 
        if not iso.exists():
            print("❌ ISO file not found.")
            return
        cmd += ["-cdrom", str(iso), "-boot", "d"]
        # -cdrom <iso> → attach ISO like a CD/DVD drive
        # -boot d → boot from CD/DVD first (so the installer starts)

    try:
        subprocess.Popen(cmd) # -> returns control to user while VM runs
        print("✅ VM launched.")
        if iso_path:
            print("👉 Ubuntu installer should boot now. Install Ubuntu onto the qcow2 disk.")
            print("👉 After installation, run again but press Enter for ISO to boot from disk.")
    except Exception as e:
        print("❌ VM launch failed.")
        print(str(e))



def create_vm_from_config():
    ok1, _, _ = run(["qemu-img", "--version"])
    ok2, _, _ = run(["qemu-system-x86_64", "--version"])
    if not (ok1 and ok2):
        print("❌ QEMU not found. Install QEMU first.")
        return

    cfg_path = input("Config path (example: ./configs/vm_config.json): ").strip()
    p = Path(cfg_path).expanduser().resolve()
    if not p.exists():
        print("❌ Config file not found.")
        return

    try:
        cfg = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print("❌ Config is not valid JSON.")
        print(str(e))
        return

    # Required inputs only
    for k in ["name", "cpu", "memory_mb", "disk_gb", "disk_path"]:
        if k not in cfg:
            print(f"❌ Missing key in config: {k}")
            return

    try:
        name = str(cfg["name"])
        cpu = int(cfg["cpu"])
        mem = int(cfg["memory_mb"])
        disk_gb = int(cfg["disk_gb"])
        disk_path = str(cfg["disk_path"])
    except ValueError:
        print("❌ Config has invalid number values.")
        return

    if cpu <= 0 or mem <= 0 or disk_gb <= 0:
        print("❌ CPU/memory/disk must be positive.")
        return

    iso_path = str(cfg.get("iso_path", "")).strip()
    iso_path = iso_path.strip('"').strip("'")

    ok, out, err = run(["qemu-img", "create", "-f", "qcow2", disk_path, f"{disk_gb}G"]) #-> create VM qcow2 disk image
    if not ok:
        print("❌ Disk creation failed.")
        print(err or out)
        return

    print(f"✅ VM '{name}' created from config.")

    cmd = ["qemu-system-x86_64", "-m", str(mem), "-smp", str(cpu), "-hda", disk_path] # -> qemu-system-x86_64 -m 2048 -smp 2 -hda ./vm1.qcow2

    if iso_path:
        iso = Path(iso_path).expanduser().resolve()
        if not iso.exists():
            print("❌ ISO file not found.")
            print(f"Path used: {iso}")
            return
        cmd += ["-cdrom", str(iso), "-boot", "d"]
        # -cdrom <iso> → attach ISO like a CD/DVD drive
        # -boot d → boot from CD/DVD first (so the installer starts)

    try:
        subprocess.Popen(cmd) # -> returns control to user while VM runs
        print("✅ VM launched.")
        if iso_path:
            print("👉 Ubuntu installer should boot now. Install Ubuntu onto the qcow2 disk.")
            print("👉 After install, remove iso_path from config (or set it to empty) to boot from disk.")
    except Exception as e:
        print("❌ VM launch failed.")
        print(str(e))



# --------------------
# Menus (simple User Interface)
# --------------------
def docker_menu():
    while True:
        print("\n--- Docker Menu ---")
        print("1) Create Dockerfile")
        print("2) Build image")
        print("3) List images")
        print("4) List running containers")
        print("5) Stop a container")
        print("6) Search local images")
        print("7) Search DockerHub")
        print("8) Pull image from DockerHub")
        print("0) Back")

        c = input("Choose: ").strip()

        if c == "1":
            create_dockerfile()
        elif c == "2":
            build_image()
        elif c == "3":
            list_images()
        elif c == "4":
            list_running_containers()
        elif c == "5":
            stop_container()
        elif c == "6":
            search_local_images()
        elif c == "7":
            search_dockerhub()
        elif c == "8":
            pull_image()
        elif c == "0":
            return
        else:
            print("Invalid option.")


def vm_menu():
    while True:
        print("\n--- VM (QEMU) Menu ---")
        print("1) Create VM (interactive)")
        print("2) Create VM (from config file)")
        print("0) Back")

        c = input("Choose: ").strip()

        if c == "1":
            create_vm_interactive()
        elif c == "2":
            create_vm_from_config()
        elif c == "0":
            return
        else:
            print("Invalid option.")


def main():
    while True:
        print("\n=== Cloud Management System ===")
        print("1) Docker operations")
        print("2) VM operations (QEMU)")
        print("0) Exit")

        c = input("Choose: ").strip()

        if c == "1":
            docker_menu()
        elif c == "2":
            vm_menu()
        elif c == "0":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
