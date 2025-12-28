# User Manual — Cloud Management System

## 0) What this project is (simple explanation)
This project is a menu-based Python program that runs in the terminal. It allows you to do two groups of tasks:
- Docker tasks (Dockerfile, build, list, search, pull, containers)
- VM tasks using QEMU (create a VM disk and launch QEMU using interactive input or a JSON config file)

Important note: When QEMU opens, you may see “Boot failed / No bootable device”. This is normal because the VM disk is empty and we did not attach an OS ISO. The project requirement is to create the disk and launch QEMU, not to install an operating system.

---

## 1) Install and setup (Windows)
You need three main tools: Python, Docker Desktop, and QEMU.

Step A — Install Python
1) Install Python 3.x (example: Python 3.11).
2) During installation, make sure “Add Python to PATH” is checked.
3) After installing, restart VS Code or your terminal.
4) Verify Python works by running this in PowerShell:
python --version

## 2) Install Docker Desktop
1) Install Docker Desktop (Windows).
2) Open Docker Desktop and wait until it shows it is running.
3) Verify Docker works by running these in PowerShell:
docker --version
docker ps

## 3) Install Qemu
1) Install QEMU for Windows.
2) Make sure QEMU is added to PATH, so the commands work in any terminal.
3) Restart VS Code / terminal after adding PATH.
4) Verify QEMU works by running these in PowerShell:
qemu-img --version
qemu-system-x86_64 --version

## 4) Open the project correctly (folder + terminal)
1) Open the project folder in VS Code.
2) Open the VS Code terminal (PowerShell).
3) Make sure you are in the project folder. Your path should end with Cloud-Management-System (the folder that contains main.py).
4) If you are not in the correct folder, use cd to go there, for example:
cd "C:\Users\HP\Desktop\Cloud Management System\Cloud-Management-System"
dir

## 5) How to run the program
From the folder that contains main.py. In powershell, run:
python main.py

You will see a main menu:

1. Docker operations
2. VM operations (QEMU)
3. Exit
   Type the number you want and press Enter.

## 6) Docker operations (Main menu option 1)
When you choose Docker operations, you will see a Docker menu. These are the actions and what they do.

Create Dockerfile
- The program asks for a Dockerfile path (example: ./Dockerfile).
- Then you type the Dockerfile lines one by one.
- Type EOF on a new line to finish.
- The program saves the Dockerfile at the chosen path.

Build image
- The program asks for the Dockerfile path and an image tag (example: myapp:1.0).
- It builds the image using Docker build.

List images
- Prints the output of docker images.

List running containers
- Prints the output of docker ps.

Stop a container
- Asks for container ID or container name.
- Stops the container using docker stop.

Search local images
- Asks for a substring to search (example: nginx).
- Searches images already on your computer (not online) and prints matches.

Search DockerHub
- Asks for a search term (example: nginx).
- Searches DockerHub online and prints results.

Pull image from DockerHub
- Asks for an image name (example: nginx:latest).
- Pulls the image using docker pull.

- General Docker Commands:
1. docker build -t <IMAGE_TAG> -f <DOCKERFILE_PATH> <BUILD_CONTEXT_FOLDER> -> Builds docker image
2. docker images -> List images
3. docker ps -> List running containers
4. docker stop <CONTAINER_ID_OR_NAME> -> Stops a container
5. docker images --format "{{.Repository}}:{{.Tag}}\t{{.ID}}\t{{.Size}}" -> Search for local images
6. docker search <SEARCH_TERM> -> Search for images on Dockerhub
7. docker pull <IMAGE_NAME:TAG> -> pull images from DockerHub


## 7) VM operations (QEMU) (Main menu option 2)
When you choose VM operations, you will see a VM menu with two important actions.

Important note about QEMU boot messages
When QEMU opens, it may show “Boot failed / No bootable device”. This is normal because we created an empty disk and did not attach an OS installer. For this project, success means:
- The .qcow2 disk file was created
- QEMU was launched

Create VM (interactive)
- The program asks you for: VM name, CPU cores, memory (MB), disk size (GB), and disk path.
- It creates a qcow2 disk using qemu-img.
- It launches QEMU using qemu-system-x86_64.

Example inputs:
- VM name: vm1
- CPU cores: 2
- Memory MB: 2048
- Disk GB: 10
- Disk path: vm1.qcow2

Create VM (from config file)
The program asks for a config file path (example: .\configs\vm_config.json).
The JSON file must include these keys:
- name
- cpu
- memory_mb
- disk_gb
- disk_path
- The program reads the JSON, creates the qcow2 disk, then launches QEMU.
{
  "name": "vm2",
  "cpu": 2,
  "memory_mb": 2048,
  "disk_gb": 20,
  "disk_path": "vm2_from_config.qcow2"
}

## 8) VERY IMPORTANT: Do not push VM disk files to GitHub
QEMU disk files can be large. Do not commit them to GitHub.

1. Add these lines to your .gitignore file:
*.qcow2
*.iso
*.img

2. Delete qcow2 files before pushing. From the project folder, run:
del *.qcow2

note: If the delete fails, it means QEMU is still using the file. Close the QEMU window (or end QEMU in Task Manager) and run the delete command again.