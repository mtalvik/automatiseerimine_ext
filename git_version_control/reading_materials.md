# 📚 Week 9: Git Reading Materials (Homework Task 2)

**Estimated Reading Time:** 2-3 hours  
**Due:** Before next class session

---

## 📖 Required Reading (1.5 hours)

### 1. Git History and Evolution (30 min)
**Source:** Git Documentation & History

**Key Topics:**
- Linus Torvalds and the creation of Git
- Why Git was needed for Linux kernel development
- Git vs other version control systems (SVN, Mercurial)
- The distributed nature of Git

**Reading Questions:**
- What problem was Git created to solve?
- How does Git's distributed nature differ from centralized VCS?
- Why did Linus Torvalds choose the name "Git"?

### 2. Git Internals Deep Dive (45 min)
**Source:** Git Internals Documentation

**Key Topics:**
- Git's object model (blobs, trees, commits, tags)
- How Git stores data (content-addressable storage)
- The .git directory structure
- Git's three-stage architecture (working directory, staging area, repository)

**Reading Questions:**
- What are the four main object types in Git?
- How does Git achieve content-addressable storage?
- What happens when you run `git add` vs `git commit`?

### 3. Advanced Branching Strategies (30 min)
**Source:** Git Flow, GitHub Flow Documentation

**Key Topics:**
- Git Flow vs GitHub Flow
- Feature branch workflow
- Release management strategies
- Hotfix procedures

**Reading Questions:**
- What are the main differences between Git Flow and GitHub Flow?
- When would you use a hotfix branch?
- How do you decide which branching strategy to use?

---

## 📚 Optional Reading (1 hour)

### 4. Git Best Practices (30 min)
**Source:** Industry Standards & Git Documentation

**Key Topics:**
- Commit message conventions
- Branch naming conventions
- When to commit vs when to stash
- Code review best practices

### 5. Git Tools and Ecosystem (30 min)
**Source:** Git Tools Documentation

**Key Topics:**
- Git GUI tools (GitKraken, SourceTree, GitHub Desktop)
- Git hosting platforms (GitHub, GitLab, Bitbucket)
- Git hooks and automation
- Git aliases and productivity tips

---

## 📋 Reference Materials (Keep Handy)

### Git Command Quick Reference
```bash
# Basic workflow
git status                    # Check repository status
git add <file>               # Stage changes
git commit -m "message"      # Commit staged changes
git push origin <branch>     # Push to remote

# Branching
git branch <name>            # Create new branch
git checkout <branch>        # Switch to branch
git merge <branch>           # Merge branch into current
git rebase <branch>          # Rebase current on branch

# History and inspection
git log --oneline           # Compact commit history
git diff                    # Show unstaged changes
git diff --staged           # Show staged changes
git show <commit>           # Show commit details
```

### Common Git Scenarios
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Create and switch to new branch
git checkout -b feature/new-feature

# Stash changes temporarily
git stash
git stash pop

# View remote repositories
git remote -v
```

---

## 🎯 Reading Reflection Assignment

After completing the reading, please submit a brief reflection (200-300 words) covering:

1. **Key Insights:** What was the most surprising or important thing you learned?
2. **Questions:** What concepts are still unclear or need more explanation?
3. **Application:** How do you think this knowledge will help in your automation work?
4. **Further Learning:** What Git topics would you like to explore more?

**Submission Format:** Add to your GitHub repository as `git_reading_reflection.md`

---

## 🔗 Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Flow Model](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

## 📝 Notes for Next Class

Come prepared with:
- Questions from your reading
- Any Git scenarios you'd like to practice
- Ideas for your final Git project
