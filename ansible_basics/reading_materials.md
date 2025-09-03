# 📚 Week 11: Ansible Reading Materials (Homework Task 2)

**Estimated Reading Time:** 2-3 hours  
**Due:** Before next class session

---

## 📖 Required Reading (1.5 hours)

### 1. Ansible Architecture Deep Dive (45 min)
**Source:** Ansible Documentation & Architecture Guide

**Key Topics:**
- Agentless architecture and its advantages
- Control node vs managed nodes
- SSH-based communication
- Ansible's execution model
- Inventory management concepts

**Reading Questions:**
- Why does Ansible use an agentless architecture?
- What are the advantages and disadvantages of agentless vs agent-based systems?
- How does Ansible handle authentication and authorization?
- What happens during an Ansible playbook execution?

### 2. YAML Syntax and Best Practices (30 min)
**Source:** YAML Documentation & Ansible Style Guide

**Key Topics:**
- YAML data types and structures
- Indentation and formatting rules
- Ansible-specific YAML conventions
- Common YAML pitfalls and how to avoid them
- YAML validation tools

**Reading Questions:**
- What are the key differences between YAML and JSON?
- Why is indentation so important in YAML?
- What are some common YAML syntax errors?
- How can you validate YAML syntax?

### 3. Ansible Module Ecosystem (30 min)
**Source:** Ansible Module Documentation

**Key Topics:**
- Core modules vs community modules
- Module categories (system, network, cloud, etc.)
- Module parameters and return values
- Idempotency in Ansible modules
- Custom module development basics

**Reading Questions:**
- What makes a module "idempotent"?
- How do you find the right module for a task?
- What's the difference between core and community modules?
- When might you need to create a custom module?

---

## 📚 Optional Reading (1 hour)

### 4. Ansible Best Practices (30 min)
**Source:** Ansible Best Practices Guide

**Key Topics:**
- Playbook organization and structure
- Variable naming conventions
- Error handling strategies
- Performance optimization techniques
- Security considerations

### 5. Ansible vs Other Configuration Management Tools (30 min)
**Source:** Industry Comparisons & Documentation

**Key Topics:**
- Ansible vs Puppet vs Chef vs Salt
- Use cases for each tool
- Learning curve comparisons
- Community and ecosystem differences
- When to choose Ansible over alternatives

---

## 📋 Reference Materials (Keep Handy)

### Ansible Command Quick Reference
```bash
# Basic commands
ansible --version              # Check Ansible version
ansible all -m ping            # Test connectivity to all hosts
ansible all -m setup           # Gather facts from all hosts
ansible-playbook playbook.yml  # Run a playbook

# Inventory management
ansible-inventory --list       # Show inventory structure
ansible-inventory --graph      # Show inventory as graph

# Ad-hoc commands
ansible webservers -m copy -a "src=/local/file dest=/remote/file"
ansible dbservers -m service -a "name=mysql state=started"
ansible all -m shell -a "uptime"
```

### Common YAML Patterns in Ansible
```yaml
# Basic playbook structure
---
- name: Example playbook
  hosts: webservers
  become: yes
  vars:
    app_name: myapp
    app_port: 8080
  
  tasks:
    - name: Install packages
      apt:
        name: "{{ item }}"
        state: present
      loop:
        - nginx
        - python3
        - git
    
    - name: Start service
      service:
        name: nginx
        state: started
        enabled: yes
```

### Ansible Facts and Variables
```yaml
# Using facts
- name: Display system info
  debug:
    msg: "{{ ansible_distribution }} {{ ansible_distribution_version }}"

# Custom variables
- name: Set custom variable
  set_fact:
    app_path: "/opt/{{ app_name }}"

# Variable precedence
# 1. extra vars (command line)
# 2. task vars
# 3. block vars
# 4. role and include vars
# 5. play vars
# 6. host facts
# 7. host vars
# 8. group vars
# 9. inventory vars
# 10. role defaults
```

---

## 🎯 Reading Reflection Assignment

After completing the reading, please submit a brief reflection (200-300 words) covering:

1. **Key Insights:** What was the most surprising or important thing you learned about Ansible?
2. **Questions:** What Ansible concepts are still unclear or need more explanation?
3. **Application:** How do you think Ansible's agentless architecture will benefit your automation work?
4. **Further Learning:** What Ansible topics would you like to explore more?

**Submission Format:** Add to your GitHub repository as `ansible_basics_reading_reflection.md`

---

## 🔗 Additional Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Ansible Module Index](https://docs.ansible.com/ansible/latest/modules/modules_by_category.html)
- [YAML Documentation](https://yaml.org/spec/)
- [Ansible Galaxy](https://galaxy.ansible.com/)

---

## 📝 Notes for Next Class

Come prepared with:
- Questions from your reading
- Any Ansible scenarios you'd like to practice
- Ideas for your Ansible automation project
- Understanding of YAML syntax and structure
