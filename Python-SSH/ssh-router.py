# Import necessary modules
import serial  # Used for serial communication with the device
import time    # Used for adding delays and timing control

# Function to collect user input for interfaces and device settings
def get_user_input():
    # Gather details for three interfaces (name, IP address, subnet mask)
    intf1 = input("Enter the first interface (e.g., Gig0/1 or Gig0/1.30): ")
    ip1 = input("Enter the IP address of the first interface (x.x.x.x): ")
    sub1 = input("Enter the subnet mask of the first interface (x.x.x.x): ")

    intf2 = input("Enter the second interface (e.g., Gig0/1 or Gig0/1.30): ")
    ip2 = input("Enter the IP address of the second interface (x.x.x.x): ")
    sub2 = input("Enter the subnet mask of the second interface (x.x.x.x): ")

    intf3 = input("Enter the third interface (e.g., Gig0/1 or Gig0/1.40): ")
    ip3 = input("Enter the IP address of the third interface (x.x.x.x): ")
    sub3 = input("Enter the subnet mask of the third interface (x.x.x.x): ")

    # Gather SSH and device login information
    username = input("Enter username: ")
    password = input("Enter password: ")
    hostname = input("Enter device hostname: ")
    com_port = input("Enter COM port: ")
    baud_rate = input("Enter baud rate (default 9600): ") or "9600"
    domain_name = input("Enter domain name: ")

    # Return all gathered inputs
    return username, password, hostname, com_port, int(baud_rate), domain_name, (intf1, ip1, sub1), (intf2, ip2, sub2), (intf3, ip3, sub3)

# Function to send a command over serial and optionally print the response
def send_command(ser, command, wait_time=1, expect_prompt=True):
    """Send a command and wait for the router response."""
    ser.write(command.encode() + b'\n')  # Send the command followed by newline
    time.sleep(wait_time)  # Wait for the device to respond
    
    if expect_prompt:
        response = ser.read(ser.in_waiting).decode(errors='ignore')  # Read the response
        print(response.strip())  # Print response for debugging
        return response

# Function to wait until a specific prompt appears (used to ensure router is ready)
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
        time.sleep(0.5)

# Function to configure an interface with IP and subnet
def configure_interface(ser, intf, ip, sub):
    print(f"Configuring interface {intf}...")

    send_command(ser, 'enable', wait_time=2)
    wait_for_prompt(ser)

    send_command(ser, 'configure terminal', wait_time=2)
    wait_for_prompt(ser, "(config)#")

    # If it's a subinterface (e.g., Gig0/1.30), handle VLAN encapsulation
    if '.' in intf:
        base_intf, vlan = intf.split('.')
        send_command(ser, f'interface {base_intf}')
        send_command(ser, 'no shutdown')  # Ensure physical interface is up
        send_command(ser, 'exit')
        wait_for_prompt(ser, "(config)#")

        send_command(ser, f'interface {base_intf}.{vlan}')
        send_command(ser, f'encapsulation dot1Q {vlan}')
    else:
        send_command(ser, f'interface {intf}')

    # Assign IP and bring up the interface
    send_command(ser, f'ip address {ip} {sub}')
    send_command(ser, 'no shutdown')
    send_command(ser, 'exit')
    wait_for_prompt(ser, "(config)#")

    send_command(ser, 'end')
    wait_for_prompt(ser, "#")

    print(f"Interface {intf} configured successfully.")

# Function to configure SSH on the device
def configure_ssh(ser, username, password, hostname, domain_name):
    print("Configuring SSH...")

    send_command(ser, 'enable', wait_time=2)
    wait_for_prompt(ser)

    send_command(ser, 'configure terminal', wait_time=2)
    wait_for_prompt(ser, "(config)#")

    # Set hostname and domain name
    send_command(ser, f'hostname {hostname}')
    send_command(ser, f'ip domain-name {domain_name}')

    # Create user credentials
    send_command(ser, f'username {username} privilege 15 secret {password}')
    wait_for_prompt(ser, "(config)#")

    # Generate RSA keys
    send_command(ser, 'crypto key generate rsa', wait_time=2)
    wait_for_prompt(ser, "How many bits in the modulus")

    send_command(ser, '1024', wait_time=5)
    wait_for_prompt(ser, "(config)#")

    # Enable SSH version 2 and configure VTY lines
    send_command(ser, 'ip ssh version 2')
    send_command(ser, 'line vty 0 4')
    send_command(ser, 'transport input ssh')
    send_command(ser, 'login local')
    send_command(ser, 'end')
    wait_for_prompt(ser, "#")

    # Save the configuration
    send_command(ser, 'write memory', wait_time=2)
    wait_for_prompt(ser, "#")

    print("SSH configuration completed successfully.")

# Main block to run the script
if __name__ == "__main__":
    # Get all inputs from the user
    user
