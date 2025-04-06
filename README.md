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

## 🤖 Phase 2: Ansible Automation
After the initial device setup via the Python scripts, this phase uses Ansible to apply complete configurations over SSH.

### 🛠 Requirements
Make sure Ansible is installed:
sudo apt install ansible
or
pip install ansible

Also install the Cisco Ansible collection for IOS:
ansible-galaxy collection install cisco.ios

### What the Playbooks Do
Each playbook configures a device over SSH, automating:

Redundant routing with HSRP
DHCP hosted on routers
Etherchanneling
VLANs and trunking (for switches)


### 🧩 Inventory (hosts)
This is where you specify the devices you want to be able to automate and their reachable IP-address + ssh creds


### 📁 Group Variables (group_vars/all.yml)
The all.yml is just a big file with all different variables in it which are used by the different playbooks.

### ▶️ Running a Playbook
To run a specific playbook e.g:
ansible-playbook -i hosts playbooks/Router-North1.yml

To target a specific group IP or group can also be hardcoded into the playbook under hosts:
ansible-playbook -i hosts playbooks/Switch-South2.yml -l switches

To preview changes without applying them:
ansible-playbook -i hosts playbooks/Router-North2.yml --check --diff

There is already some hosts in the hosts file and hardcoded into the playbooks, just switch these out with the ones from your enviroment. 
