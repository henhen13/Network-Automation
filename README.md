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

### 🗂️ Project Structure
Network-Automation-main/
├── ansible.cfg               # Ansible configuration file
├── hosts                     # Inventory file
├── group_vars/
│   └── all.yml               # Global variables
├── playbooks/
│   ├── Router-North1.yml
│   ├── Router-North2.yml
│   └── Switch-South2.yml

### 🛠 Requirements

Make sure Ansible is installed:

```bash
sudo apt install ansible
# or
pip install ansible

Also install the Cisco Ansible collection:
bashCopyansible-galaxy collection install cisco.ios
🔧 What the Playbooks Do
Each playbook configures a device over SSH, automating:

Hostname and banner messages
Interface descriptions and IP settings
VLANs and trunking (for switches)
Routing (for routers)
NTP, syslog, and SNMP
Passwords and SSH user settings

🧩 Example Inventory (hosts)
iniCopy[switches]
192.168.1.10

[routers]
192.168.1.1
192.168.1.2
📁 Example Group Variables (group_vars/all.yml)
yamlCopyansible_connection: network_cli
ansible_network_os: cisco.ios.ios
ansible_user: admin
ansible_password: cisco123
ansible_become: yes
ansible_become_method: enable
ansible_become_password: cisco123
▶️ Running a Playbook
To run a specific playbook:
bashCopyansible-playbook -i hosts playbooks/Router-North1.yml
To target a specific group:
bashCopyansible-playbook -i hosts playbooks/Switch-South2.yml -l switches
To preview changes without applying them:
bashCopyansible-playbook -i hosts playbooks/Router-North2.yml --check --diff
🔄 Full Automation Flow

Use Python script to enable SSH on the device via console.
Add the device IP to the hosts inventory file.
Set login credentials in group_vars/all.yml.
Run your Ansible playbook.
Done! 🎉

🧠 Tips

Test SSH access manually before running playbooks.
Keep configs modular with roles (optional for bigger setups).
You can run multiple playbooks in one go or create a master playbook.
