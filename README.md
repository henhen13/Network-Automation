# ⚙️ Network Automation 

This repository provides a two-phase setup for automating Cisco network device configuration:

1. **Python Console Scripts** – For initial setup and enabling SSH access via console cable.  
2. **Ansible Playbooks** – For automating further configuration over SSH.

Whether you're provisioning a lab or streamlining your production setup, this repo gets your devices online and Ansible-ready in minutes.

---

## 🐍 Phase 1: Python Console Setup

These Python scripts are used to prepare **Cisco routers and switches** for automation by:

- Configuring basic interfaces  
- Setting hostnames  
- Enabling and securing SSH access  

### 📁 Scripts

- `ssh-switch.py` – Console-based config for switches  
- `ssh-router.py` – Console-based config for routers

### 🚀 What It Does

- Connects over a **console cable**
- Prompts for:
  - Interface name
  - IP address / subnet
  - Hostname
  - SSH credentials
- Applies configuration to enable basic connectivity and SSH
- Saves the config to startup

### ⚠️ Important Setup Note

These scripts **assume you're past the initial configuration dialog**. Before running:

1. Connect via terminal (e.g., PuTTY, minicom)
2. When asked: Would you like to enter the initial configuration dialog? [yes/no]:
3. Type "no"
4. Wait until the CLI appears (`Switch>`, `Router>`), then run the script.


