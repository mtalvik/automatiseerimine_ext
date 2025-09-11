# Vagrant Setup Guide

## Ülevaade
Vagrant on virtuaalmasinate haldamise tööriist. Võimaldab kiiresti seadistada ja jagada arenduskeskkondi.

## Prereq'id
- Windows 10/11 Pro (Hyper-V support)
- 8GB+ RAM (soovituslik)
- BIOS'is virtualization enabled

## Install

### VirtualBox
```bash
winget install Oracle.VirtualBox
```
Või laadi `virtualbox.org`

### Vagrant  
```bash
winget install Hashicorp.Vagrant
```
Või laadi `vagrantup.com`

**Restart after install!**

## Quick Start

```bash
# Create project
mkdir dev-env && cd dev-env

# Initialize Vagrantfile
vagrant init ubuntu/jammy64

# Start VM
vagrant up

# SSH into VM
vagrant ssh

# Exit VM
exit

# Stop VM
vagrant halt
```

## Vagrantfile Template

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  
  # Network
  config.vm.network "private_network", ip: "192.168.56.10"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  
  # Resources
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
  end
  
  # Auto-setup
  config.vm.provision "shell", inline: <<-SHELL
    apt update && apt upgrade -y
    apt install -y git curl vim nginx
    systemctl start nginx
  SHELL
  
  # Shared folder
  config.vm.synced_folder ".", "/vagrant"
end
```

## Essential Commands

| Command | Action |
|---------|--------|
| `vagrant up` | Start VM |
| `vagrant halt` | Stop VM |
| `vagrant reload` | Restart VM |
| `vagrant ssh` | Connect via SSH |
| `vagrant destroy` | Delete VM |
| `vagrant status` | Check status |
| `vagrant suspend` | Pause VM |
| `vagrant resume` | Resume paused VM |

## Common Boxes

```bash
# Ubuntu 22.04
vagrant init ubuntu/jammy64

# CentOS 7
vagrant init centos/7

# Alpine Linux (minimal)
vagrant init generic/alpine316

# Windows Server (if needed)
vagrant init gusztavvargadr/windows-server
```

## Networking Options

```ruby
# Port forwarding
config.vm.network "forwarded_port", guest: 3000, host: 3000

# Private network (host-only)
config.vm.network "private_network", ip: "192.168.56.10"

# Public network (bridged)
config.vm.network "public_network"
```

## Provisioning

### Shell Script
```ruby
config.vm.provision "shell", path: "setup.sh"
```

### Inline Commands
```ruby
config.vm.provision "shell", inline: <<-SHELL
  apt update
  apt install -y docker.io
  usermod -aG docker vagrant
SHELL
```

## Multi-Machine Setup

```ruby
Vagrant.configure("2") do |config|
  # Web server
  config.vm.define "web" do |web|
    web.vm.box = "ubuntu/jammy64"
    web.vm.network "private_network", ip: "192.168.56.10"
  end
  
  # Database server  
  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/jammy64"
    db.vm.network "private_network", ip: "192.168.56.11"
  end
end
```

## Troubleshooting

### Hyper-V Conflict
```powershell
# Run as admin
bcdedit /set hypervisorlaunchtype off
# Restart required
```

### Performance Issues
```ruby
config.vm.provider "virtualbox" do |vb|
  vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
end
```

### SSH Issues
```bash
# Re-add SSH key
vagrant ssh-config
```

## Useful Plugins

```bash
# Better provisioning
vagrant plugin install vagrant-reload

# Disk size management  
vagrant plugin install vagrant-disksize

# Host manager
vagrant plugin install vagrant-hostmanager
```

## Best Practices

- Keep Vagrantfiles in version control
- Use `.vagrant/` in `.gitignore`
- Document custom provisioning
- Use shared folders for development
- Snapshot important states: `vagrant snapshot save name`

## Example Development Setup

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.network "private_network", ip: "192.168.56.10"
  
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 2
  end
  
  # Development tools
  config.vm.provision "shell", inline: <<-SHELL
    # Node.js LTS
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    apt-get install -y nodejs
    
    # Docker
    curl -fsSL https://get.docker.com | sh
    usermod -aG docker vagrant
    
    # VS Code Server (optional)
    wget -O- https://aka.ms/install-vscode-server/setup.sh | sh
  SHELL
  
  config.vm.synced_folder "./projects", "/home/vagrant/projects"
end
```

## Resources
- [Official Docs](https://www.vagrantup.com/docs)
- [Vagrant Cloud](https://app.vagrantup.com/boxes/search)
- [Community Boxes](https://app.vagrantup.com/)

🦍 Better for teenagers who actually know what they're doing!
