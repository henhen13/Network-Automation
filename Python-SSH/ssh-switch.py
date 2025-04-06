# Import required libraries
import serial  # For serial communication with network devices
import time    # To handle delays and waiting between commands

# Function to collect input from the user
def get_user_input():
    # Ask if user wants to configure trunk/access interfaces
    configure_interfaces = input("Do you need to configure the interfaces? (yes/no): ").strip().lower()

    # Management VLAN settings
    mgmt_vlan = input("Enter the VLAN where SSH should be set up (e.g., 99): ")
    mgmt_vlan_name = input("Enter the name for the management VLAN: ")

    # Interface connections (trunks or client access)
    mgmt_intR1 = input("Enter the first trunk interface (or 'none' to skip): ")
    mgmt_intR2 = input("Enter the second trunk interface (or 'none' to skip): ")
    mgmt_intR3 = input("Enter the third trunk interface (or 'none' to skip): ")
    mgmt_intC = input("Enter the interface which goes to the client (or 'none' to skip): ")

    # IP configuration for VLAN interface
    mgmt_ip = input("Enter the IP address of the SSH interface (x.x.x.x): ")
    mgmt_sub = input("Enter the subnet mask of the SSH interface (x.x.x.x): ")
    default_gw = input("Enter the switch's default gateway: ")

    # SSH login and device identification
    username = input("Enter username: ")
    password = input("Enter password: ")
    hostname = input("Enter device host name: ")
    com_port = input("Enter COM port: ")
    baud_rate = input("Enter baud rate (default 9600): ")
    domain_name = input("Enter domain name: ")

    # Return all inputs for further processing
    return configure_interfaces, username, password, hostname, com_port, baud_rate, domain_name, mgmt_vlan, mgmt_vlan_name, mgmt_ip, mgmt_sub, mgmt_intR1, mgmt_intR2, mgmt_intR3, mgmt_intC, default_gw

# Function to send a command to the serial port and optionally read the output
def send_command(ser, command, wait_time=1, expect_prompt=True):
    """Send a command and wait for the router/switch response."""
    ser.write(command.encode() + b'\n')  # Send command to the device
    time.sleep(wait_time)  # Allow device time to respond
    
    if expect_prompt:
        response = ser.read(ser.in_waiting).decode(errors='ignore')  # Read response
        print(response.strip())  # Display response (for debugging/logging)
        return response

# Function to wait until a specific prompt is seen (used to sync with device CLI)
def wait_for_prompt(ser, expected_prompt="#", timeout=5):
    """Wait for the router to return to the prompt before sending more commands."""
    start_time = time.time()
    while True:
        response = ser.read(ser.in_waiting).decode(errors='ignore')
        if expected_prompt in response:
            print(response.strip())  # Debugging output
            return True
        if time.time() - start_time > timeout:
            print("Warning: Timeout waiting for prompt.")
            return False
        time.sleep(0.5)  # Check again after a short delay

# Main function to configure SSH and optionally the interfaces
def configure_ssh(configure_interfaces, username, password, hostname, com_port, baud_rate, domain_name,
                  mgmt_vlan, mgmt_vlan_name, mgmt_ip, mgmt_sub, mgmt_intR1, mgmt_intR2, mgmt_intR3, mgmt_intC, default_gw):
    try:
        # Open serial connection with the switch/router
        with serial.Serial(com_port, baud_rate, timeout=1) as ser:
            time.sleep(2)  # Give time for the connection to stabilize

            # Enter privileged and global config mode
            send_command(ser, 'enable')
            send_command(ser, 'configure terminal')

            # Configure trunk and access interfaces if user selected "yes"
            if configure_interfaces == 'yes':
                if mgmt_intR1.lower() != 'none':
                    send_command(ser, f'interface {mgmt_intR1}')
                    send_command(ser, 'switchport mode trunk')
                    send_command(ser, 'exit')
                if mgmt_intR2.lower() != 'none':
                    send_command(ser, f'interface {mgmt_intR2}')
                    send_command(ser, 'switchport mode trunk')
                    send_command(ser, 'exit')
                if mgmt_intR3.lower() != 'none':
                    send_command(ser, f'interface {mgmt_intR3}')
                    send_command(ser, 'switchport mode trunk')
                    send_command(ser, 'exit')
                if mgmt_intC.lower() != 'none':
                    send_command(ser, f'interface {mgmt_intC}')
                    send_command(ser, f'switchport access vlan {mgmt_vlan}')
                    send_command(ser, 'exit')

            # Create and name the management VLAN
            send_command(ser, f'vlan {mgmt_vlan}')
            send_command(ser, f'name {mgmt_vlan_name}')
            send_command(ser, 'exit')

            # Assign IP and bring up the VLAN interface
            send_command(ser, f'interface vlan {mgmt_vlan}')
            send_command(ser, f'ip address {mgmt_ip} {mgmt_sub}')
            send_command(ser, 'no shutdown')
            send_command(ser, 'exit')

            # Set hostname, domain, and default gateway
            send_command(ser, f'hostname {hostname}')
            send_command(ser, f'ip domain-name {domain_name}')
            send_command(ser, f'ip default-gateway {default_gw}')

            # Create SSH user
            send_command(ser, f'username {username} privilege 15 secret {password}')

            # Generate RSA keys for SSH
            send_command(ser, 'crypto key generate rsa')
            send_command(ser, '1024', wait_time=5)  # Key length

            # Enable SSH v2 and configure VTY lines
            send_command(ser, 'ip ssh version 2')
            send_command(ser, 'line vty 0 4')
            send_command(ser, 'transport input ssh')
            send_command(ser, 'login local')
            send_command(ser, 'end')

            # Save configuration to memory
            send_command(ser, 'write memory', wait_time=2)

            print("SSH configuration completed successfully.")

    except Exception as e:
        print(f"Failed to configure SSH: {e}")

# Entry point of the script
if __name__ == "__main__":
    # Collect user inputs
    configure_interfaces, username, password, hostname, com_port, baud_rate, domain_name, mgmt_vlan, mgmt_vlan_name, \
    mgmt_ip, mgmt_sub, mgmt_intR1, mgmt_intR2, mgmt_intR3, mgmt_intC, default_gw = get_user_input()

    # Run SSH configuration based on provided inputs
    configure_ssh(configure_interfaces, username, password, hostname, com_port, baud_rate, domain_name,
                  mgmt_vlan, mgmt_vlan_name, mgmt_ip, mgmt_sub, mgmt_intR1, mgmt_intR2, mgmt_intR3, mgmt_intC, default_gw)
