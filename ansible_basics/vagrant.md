# 🚀 Vagrant Setup for Ansible Lab

## Windows Setup Guide

### 1. Install Required Software

```powershell
# Install VirtualBox
winget install Oracle.VirtualBox

# Install Vagrant
winget install Hashicorp.Vagrant

# RESTART WINDOWS after installation!
```

Or download manually:
- VirtualBox: https://virtualbox.org
- Vagrant: https://vagrantup.com

### 2. Create Lab Environment

```bash
# Create project folder
mkdir ansible-lab
cd ansible-lab

# Download the Vagrantfile (or create it)
# Copy the Vagrantfile content from above

# Start both VMs
vagrant up

# Check status
vagrant status
```

### 3. Access Your VMs

**Option 1: Use vagrant ssh**
```bash
# Connect to controller
vagrant ssh controller

# Connect to webserver (in new terminal)
vagrant ssh webserver
```

**Option 2: Use SSH client (PuTTY, Terminal)**
```bash
# Controller: 192.168.56.10
# Webserver: 192.168.56.11
# Username: ansible
# Password: ansible123
```

### 4. Start Ansible Lab

On controller VM:
```bash
# Switch to ansible user
sudo su - ansible

# Generate SSH key
ssh-keygen -t ed25519
# Press Enter 3 times

# Copy key to webserver
ssh-copy-id ansible@192.168.56.11
# Enter password: ansible123

# Test connection
ssh ansible@192.168.56.11
exit

# Create your first inventory
cd ~
mkdir ansible_tutorial
cd ansible_tutorial

cat > inventory.ini << 'EOF'
[local]
localhost ansible_connection=local

[webservers]
webserver ansible_host=192.168.56.11 ansible_user=ansible

[all:children]
local
webservers
EOF

# Test Ansible
ansible -i inventory.ini all -m ping
```

## VM Details

| VM | Hostname | IP | User | Password |
|----|----------|-----|------|----------|
| Controller | ansible-controller | 192.168.56.10 | ansible | ansible123 |
| Web Server | web-server | 192.168.56.11 | ansible | ansible123 |

Both VMs also have:
- User: `vagrant` (password: `vagrant`)
- Sudo access without password

## Useful Vagrant Commands

```bash
# Start VMs
vagrant up

# Stop VMs
vagrant halt

# Restart VMs
vagrant reload

# Delete VMs (careful!)
vagrant destroy

# Check status
vagrant status

# SSH to specific VM
vagrant ssh controller
vagrant ssh webserver

# See SSH config
vagrant ssh-config

# Suspend/Resume
vagrant suspend
vagrant resume
```

## File Sharing

Your Windows `ansible-lab` folder is automatically shared to `/vagrant` in both VMs.

```bash
# In VM
cd /vagrant
ls  # See your Windows files

# Copy files between Windows and VM
cp /vagrant/myfile.yml ~/
```

## Troubleshooting

### VirtualBox Error
```powershell
# If Hyper-V conflict (run as admin)
bcdedit /set hypervisorlaunchtype off
# Restart Windows
```

### SSH Connection Issues
```bash
# Regenerate SSH keys
vagrant ssh-config > config
ssh -F config controller
```

### VM Won't Start
```bash
# Check VirtualBox
VBoxManage list vms

# Force cleanup
vagrant destroy -f
vagrant up
```

### Network Issues
- Make sure Windows Firewall isn't blocking
- Check VirtualBox network adapter settings
- Try different IP range (192.168.33.x)

## Next Steps

1. Complete the Ansible lab exercises
2. Your code in `/vagrant` is shared between Windows and VMs
3. Use VS Code on Windows with Remote SSH extension
4. Install VS Code Remote SSH to edit files directly in VM

## Clean Up

When done with the lab:
```bash
# Save your work first!
cp -r ~/ansible_tutorial /vagrant/

# Stop VMs (can start again later)
vagrant halt

# OR completely remove VMs
vagrant destroy
```

## Tips

- Use Git Bash on Windows for better terminal experience
- Install Windows Terminal for multiple tabs
- VS Code with Remote SSH extension works great
- Take snapshots: `vagrant snapshot save before-lab`
- Restore snapshot: `vagrant snapshot restore before-lab`
