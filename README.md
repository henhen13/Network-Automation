🐍 Python SSH Scripts for Network Device Configuration
This project includes two Python scripts designed to automate the configuration of network devices (routers and switches) via a console cable. These scripts are useful for initial SSH setup and interface configuration — tailored for a specific topology but flexible enough for adaptation.

📂 Scripts
ssh-router.py: For configuring routers.

ssh-switch.py: For configuring switches.

⚙️ What the Scripts Do
Access network devices over a console connection.

Configure interface settings based on user input.

Automatically enable and configure SSH access.

Set hostnames, IP addresses, and more.

Save the configuration to startup.

⚠️ Important Note Before Running
These scripts do not handle the initial configuration dialog that appears when a Cisco device is powered on for the first time.
Before running either script:

Connect to the device using a console terminal (e.g., PuTTY, Tera Term, screen).

When prompted with Would you like to enter the initial configuration dialog? [yes/no]:, type no.

Then run the appropriate script.

Skipping this step may cause the script to fail or behave unpredictably.

🧑‍💻 Usage
Connect to the router or switch via a console cable.

Run the appropriate script:

bash
Copy
Edit
python ssh-switch.py
or

bash
Copy
Edit
python ssh-router.py
Follow the prompts to enter IP addresses, interface names, and credentials.

📦 Requirements
Python 3.x

pyserial (for serial/console communication)

Possibly netmiko or similar (depending on script implementation)

Install dependencies with:

bash
Copy
Edit
pip install pyserial
