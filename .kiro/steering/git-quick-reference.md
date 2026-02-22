---
inclusion: manual
contextKey: git-quick-ref
---

# Git Quick Reference for Spec-Driven Development

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `spec` - Specification changes
- `task` - Task updates
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code restructuring
- `test` - Test additions
- `docs` - Documentation
- `style` - Code formatting
- `chore` - Maintenance
- `perf` - Performance

### Example
```
feat(processor): Implement rotation detection

Implements automatic text orientation detection and
correction for images before OCR processing.

Task: 19
Requirement: 9.2, 9.3
```

---

## Branch Naming

```
<type>/<task-number>-<description>

Examples:
feature/19-rotation-detection
bugfix/aws-rate-limiting
docs/20.3-consolidate-docs
refactor/20.1-move-source-code
spec/add-requirement-10
```

---

## Common Workflows

### Start New Feature
```bash
git checkout main
git pull
git checkout -b feature/19-rotation-detection
# ... work ...
git add .
git commit -m "feat(processor): Implement rotation detection

Task: 19
Requirement: 9.2"
git push origin feature/19-rotation-detection
```

### Fix Bug
```bash
git checkout -b bugfix/aws-timeout
# ... fix ...
git commit -m "fix(aws): Increase timeout for large files

Fixes #123
Task: 3.3"
git push origin bugfix/aws-timeout
```

### Update Specs
```bash
git checkout -b spec/add-rotation-feature
# Edit requirements.md
git commit -m "spec(requirements): Add rotation detection requirement"
# Edit tasks.md
git commit -m "spec(tasks): Add rotation detection tasks"
git push origin spec/add-rotation-feature
```

---

## Daily Commands

```bash
# Start day
git checkout main
git pull

# Create branch
git checkout -b feature/task-number-description

# Check status
git status
git diff

# Stage changes
git add <files>
git add .

# Commit
git commit -m "type(scope): description"

# Push
git push origin branch-name

# Update from main
git checkout main
git pull
git checkout feature-branch
git rebase main
```

---

## Useful Commands

```bash
# View history
git log --oneline --graph

# Undo changes
git checkout -- <file>      # Discard working changes
git reset HEAD <file>        # Unstage
git reset --soft HEAD~1      # Undo commit, keep changes

# Stash
git stash                    # Save changes
git stash pop                # Restore changes

# Amend last commit
git commit --amend

# Squash commits
git rebase -i HEAD~3
```

---

## Before Committing

- [ ] Tests pass
- [ ] No secrets
- [ ] Commit message follows format
- [ ] References task/requirement

---

## Before PR

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Task marked complete
- [ ] Branch up to date
- [ ] Commits squashed

---

## Commit Message Template

Save as `.gitmessage`:
```
# <type>(<scope>): <subject>
# |<----  Max 50 chars  ---->|

# <body>
# |<----  Wrap at 72 chars  -------------------------->|

# Task: 
# Requirement: 
# Fixes: 

# Types: spec, task, feat, fix, refactor, test, docs, style, chore, perf
# Scopes: requirements, tasks, processor, generator, config, tests, docs, cli
```

Configure:
```bash
git config --global commit.template .gitmessage
```

---

## .gitignore Essentials

```gitignore
# Python
__pycache__/
*.pyc
venv/
*.egg-info/

# Environment
.env
*.key

# IDE
.vscode/
.idea/

# Output
output/
*.log

# OS
.DS_Store
```

---

## Quick Troubleshooting

**Wrong branch?**
```bash
git stash
git checkout -b correct-branch
git stash pop
```

**Undo last commit?**
```bash
git reset --soft HEAD~1  # Keep changes
git reset --hard HEAD~1  # Discard changes
```

**Merge conflict?**
```bash
# Edit files, remove markers
git add <resolved-files>
git commit
```

**Forgot to add file?**
```bash
git add <file>
git commit --amend --no-edit
```

---

## Spec-Driven Workflow

1. **Specs First**
   ```bash
   git checkout -b spec/add-feature
   # Edit requirements.md and tasks.md
   git commit -m "spec: Add feature requirement and tasks"
   # Merge to main
   ```

2. **Implementation**
   ```bash
   git checkout -b feature/task-number
   # Implement feature
   git commit -m "feat: Implement feature
   
   Task: X
   Requirement: Y"
   ```

3. **Mark Complete**
   ```bash
   # Edit tasks.md
   git commit -m "task: Mark Task X complete"
   ```

---

## Version Tags

```bash
# Create tag
git tag -a v1.0.0 -m "Release 1.0.0"

# Push tag
git push origin v1.0.0

# List tags
git tag -l
```

---

## PR Template

```markdown
## Description
Brief description of changes.

## Related Specifications
- **Requirement:** X.Y
- **Task:** Z

## Changes Made
- [ ] Item 1
- [ ] Item 2

## Type of Change
- [ ] Spec update
- [ ] New feature
- [ ] Bug fix
- [ ] Refactoring
- [ ] Documentation

## Testing
- [ ] All tests pass
- [ ] Added new tests

## Checklist
- [ ] Code follows style
- [ ] Documentation updated
- [ ] Task marked complete
```

---

**Full Guide:** `.kiro/steering/git-workflow-guide.md`

**Last Updated:** 2025-01-31
