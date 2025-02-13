import os

def setup_firewall():
    print("Setting up firewall rules...")
    
    # Flush existing rules
    os.system("iptables -F")
    os.system("iptables -X")
    os.system("iptables -Z")
    os.system("iptables -t nat -F")
    
    # Default policies: Block all inbound and outbound traffic
    os.system("iptables -P INPUT DROP")
    os.system("iptables -P OUTPUT ACCEPT")  # Allow outbound traffic
    os.system("iptables -P FORWARD DROP")
    
    # Allow inbound traffic on SSH (22), HTTP (80), HTTPS (443)
    os.system("iptables -A INPUT -p tcp --dport 22 -j ACCEPT")
    os.system("iptables -A INPUT -p tcp --dport 80 -j ACCEPT")
    os.system("iptables -A INPUT -p tcp --dport 443 -j ACCEPT")
    
    # Allow loopback interface
    os.system("iptables -A INPUT -i lo -j ACCEPT")
    os.system("iptables -A OUTPUT -o lo -j ACCEPT")
    
    # Allow established and related incoming connections
    os.system("iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT")
    
    # Log dropped packets (optional)
    os.system("iptables -A INPUT -j LOG --log-prefix 'Dropped Packet: ' --log-level 4")
    
    print("Firewall rules successfully applied!")

if __name__ == "__main__":
    setup_firewall()
