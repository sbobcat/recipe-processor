---
inclusion: manual
contextKey: git-workflow
---

# Git Workflow for Spec-Driven Development

## Purpose

This guide establishes Git best practices aligned with spec-driven development, ensuring version control supports the requirements → tasks → implementation workflow.

**📋 For commands, formats, and examples:** See `git-quick-reference.md` (`#git-quick-ref`)

**This guide covers:** Principles, patterns, and workflows  
**Quick reference covers:** Commands, formats, and daily operations

---

## Core Principles

### 1. Spec-First Commits
**Principle:** Specifications (requirements, tasks) are committed before implementation.

**Why:** Establishes clear intent and traceability before code changes.

**In Practice:**
1. Commit requirement changes first
2. Commit task updates second
3. Commit implementation third
4. Each commit references the requirement/task

### 2. Atomic Commits
**Principle:** Each commit represents one logical change.

**Why:** Makes history readable, enables easy rollback, simplifies code review.

**In Practice:**
- One task may have multiple commits
- Each commit should pass tests
- Commit messages explain the "why"
- Related changes stay together

### 3. Traceability
**Principle:** Every code change traces back to a requirement and task.

**Why:** Maintains clear connection between business needs and implementation.

**In Practice:**
- Commit messages reference task numbers
- Branch names include task identifiers
- Pull requests link to requirements
- Git history tells the project story

### 4. Clean History
**Principle:** Git history should be readable and meaningful.

**Why:** Makes debugging easier, helps new developers understand decisions.

**In Practice:**
- Meaningful commit messages
- Logical commit ordering
- Squash WIP commits before merging
- Keep main branch clean and stable

---

## Branch Strategy

### Branch Naming
**Format:** `<type>/<task-number>-<brief-description>`

**See:** `#git-quick-ref` for complete branch naming reference and examples.

### Branch Types and Usage

| Type | Purpose | Lifespan | Merge To |
|------|---------|----------|----------|
| `spec/` | Specification updates | 1-2 days | `main` |
| `feature/` | New functionality | 2-5 days | `main` |
| `bugfix/` | Bug fixes | 1-3 days | `main` |
| `refactor/` | Code restructuring | 2-5 days | `main` |
| `docs/` | Documentation only | 1-2 days | `main` |
| `test/` | Test additions | 1-2 days | `main` |
| `hotfix/` | Critical fixes | Hours | `main` immediately |

### Main Branch Protection

**`main` branch should:**
- Always be deployable
- Require pull request reviews
- Pass all CI checks before merge
- Be tagged for releases
- Never have direct commits (except hotfixes)

---

## Commit Message Strategy

### Structure
**See:** `#git-quick-ref` for complete commit message format and examples.

### Key Elements

**Type:** Categorizes the change (spec, task, feat, fix, refactor, test, docs)  
**Scope:** Indicates affected area (processor, generator, config, tests)  
**Subject:** Brief description (imperative mood, <50 chars)  
**Body:** Detailed explanation of why (wrap at 72 chars)  
**Footer:** Task/requirement references, issue links

### Writing Good Commit Messages

**Do:**
- Explain WHY, not what (code shows what)
- Use imperative mood ("Add" not "Added")
- Reference tasks and requirements
- Keep subject line under 50 characters
- Wrap body at 72 characters

**Don't:**
- Be vague ("Updated files", "Fixed bug")
- Include multiple unrelated changes
- Forget task/requirement references
- Write novels (be concise)

---

## Spec-Driven Workflow Patterns

### Pattern 1: Spec-First Feature Development

**Phase 1: Specifications**
```
1. Create spec branch
2. Add/update requirements.md
3. Add/update tasks.md
4. Commit specs with clear messages
5. Create PR, review, merge to main
```

**Phase 2: Implementation**
```
6. Create feature branch from main (now has specs)
7. Implement feature incrementally
8. Commit with task/requirement references
9. Add tests
10. Update documentation
11. Mark task complete in tasks.md
12. Create PR, review, merge
```

**See:** `#git-quick-ref` for complete command examples.

### Pattern 2: Bug Fix Workflow

**Steps:**
1. Create bugfix branch
2. Add task to tasks.md (if not exists)
3. Fix the bug
4. Add regression test
5. Mark task complete
6. Create PR with issue reference

**Key Points:**
- Always add regression test
- Reference issue number in commit
- Keep fix minimal and focused
- Update documentation if needed

### Pattern 3: Refactoring Workflow

**Steps:**
1. Ensure specs exist for refactoring
2. Create refactor branch
3. Make changes incrementally
4. Ensure tests pass after each commit
5. Update affected documentation
6. Mark tasks complete

**Key Points:**
- No functional changes during refactoring
- Tests should pass throughout
- Break large refactors into smaller PRs
- Update imports and references carefully

### Pattern 4: Documentation-Only Changes

**Steps:**
1. Create docs branch
2. Update documentation
3. Verify all links work
4. Create PR

**Key Points:**
- No code changes in docs-only PRs
- Keep documentation in sync with code
- Update examples if needed
- Check for broken links

---

## Pull Request Guidelines

### PR Structure

**Title:** `<type>: <brief description> (Task #)`

**Description Should Include:**
- What changed and why
- Related requirements and tasks
- Breaking changes (if any)
- Testing performed
- Checklist of changes

**See:** `#git-quick-ref` for complete PR template.

### PR Best Practices

**Size:**
- Keep PRs small (<400 lines preferred)
- One feature/fix per PR
- Break large changes into multiple PRs

**Review:**
- Respond to feedback within 24 hours
- Don't take feedback personally
- Explain decisions when needed
- Update based on feedback

**Merging:**
- Squash WIP commits before merge
- Ensure CI passes
- Get required approvals
- Delete branch after merge

---

## Version Control Best Practices

### What to Commit

**Always:**
- Source code
- Tests
- Documentation
- Configuration templates (`.env.example`)
- Build scripts
- Specifications (requirements.md, tasks.md)

**Never:**
- Secrets (API keys, passwords)
- Environment files (`.env`)
- Build artifacts (`dist/`, `build/`)
- Dependencies (`node_modules/`, `__pycache__/`)
- IDE files (`.vscode/`, `.idea/`)
- Large binary files (use Git LFS)

**See:** `#git-quick-ref` for complete .gitignore template.

### Commit Frequency

**Commit When:**
- Completing a logical unit of work
- Tests pass
- Before switching tasks
- At end of work session

**Don't Commit:**
- Broken code (unless WIP branch)
- Failing tests
- Multiple unrelated changes together

### When to Squash Commits

**Squash Before Merging:**
- Multiple "WIP" commits
- "Fix typo" commits
- "Oops, forgot file" commits
- Commits that don't add value to history

**Keep Separate:**
- Spec changes vs implementation
- Different logical changes
- Changes to different modules
- Commits that tell a story

---

## Tagging and Releases

### Semantic Versioning

**Format:** `vMAJOR.MINOR.PATCH`

**When to Increment:**
- **MAJOR:** Breaking changes (v2.0.0)
- **MINOR:** New features, backward compatible (v1.1.0)
- **PATCH:** Bug fixes, backward compatible (v1.0.1)

### Release Process

1. Update VERSION file
2. Update CHANGELOG.md
3. Commit version bump
4. Create annotated tag
5. Push tag to remote
6. Create GitHub release (if applicable)

**See:** `#git-quick-ref` for tagging commands.

---

## Handling Merge Conflicts

### Resolution Strategy

1. **Understand the conflict** - Review both changes
2. **Choose resolution** - Keep yours, theirs, combine, or rewrite
3. **Test after resolution** - Ensure nothing breaks
4. **Commit with clear message** - Explain resolution

### Preventing Conflicts

**Best Practices:**
- Pull frequently from main
- Keep branches short-lived (1-5 days)
- Communicate about shared files
- Coordinate major refactoring
- Review PRs promptly

**See:** `#git-quick-ref` for conflict resolution commands.

---

## Team Collaboration

### Code Review Guidelines

**For Authors:**
- Keep PRs small and focused
- Write clear PR descriptions
- Link to requirements and tasks
- Respond to feedback promptly
- Don't take feedback personally

**For Reviewers:**
- Review within 24 hours
- Be constructive and specific
- Ask questions, don't demand
- Approve when satisfied
- Check alignment with specs

### Review Checklist

**Functionality:**
- Aligns with requirements and tasks
- Edge cases handled
- Error handling appropriate

**Code Quality:**
- Readable and maintainable
- No unnecessary complexity
- Follows project conventions

**Testing:**
- Tests are comprehensive
- All tests pass
- Edge cases tested

**Documentation:**
- Code well-commented
- API documentation updated
- CHANGELOG updated

---

## Git Hooks for Validation

### Pre-Commit Hook
Validates before commit:
- No secrets in code
- No large files
- Python syntax valid (if Python files)

### Commit-Msg Hook
Validates commit message:
- Follows format: `type(scope): subject`
- Subject line length
- Required elements present

**See:** `#git-quick-ref` for hook installation and examples.

---

## Spec-Driven Git Integration

### Linking Commits to Specs

**Every commit should reference:**
1. Task number - Which task is being implemented
2. Requirement - Which requirement is being addressed

**Example:**
```
feat(processor): Implement rotation detection

Task: 19
Requirement: 9.2, 9.3, 9.7
```

### Task Status Through Git

**Track progress:**
- Task started: Commit to tasks.md marking in progress
- Task in progress: Implementation commits reference task
- Task complete: Commit to tasks.md marking complete

### Spec Changes Trigger Implementation

**Workflow:**
1. Spec changes merged to main
2. Implementation branches created from main
3. Implementation references spec commits
4. Task completion updates specs

---

## Common Scenarios

### Scenario 1: Starting a New Feature

**Steps:**
1. Check if specs exist
2. If no spec, create spec branch first
3. Create implementation branch from main
4. Implement, test, document
5. Push and create PR

**See:** `#git-quick-ref` for complete command sequence.

### Scenario 2: Emergency Hotfix

**Steps:**
1. Create hotfix branch from main
2. Make minimal fix
3. Fast-track review
4. Merge immediately
5. Tag new version
6. Document in specs after the fact

**Key Points:**
- Keep changes minimal
- Get immediate review
- Tag immediately after merge
- Update specs retroactively

### Scenario 3: Large Refactoring

**Steps:**
1. Create spec for refactoring
2. Break into smaller branches
3. Implement one task per branch
4. Merge incrementally
5. Continue until complete

**Key Points:**
- Don't do everything in one PR
- Keep main stable throughout
- Test after each merge
- Communicate with team

---

## Troubleshooting

### Common Issues

**Wrong branch?**
- Stash changes, switch branch, pop stash

**Undo last commit?**
- Soft reset to keep changes
- Hard reset to discard changes

**Merge conflict?**
- Edit files, remove markers, commit

**Forgot to add file?**
- Add file, amend last commit

**See:** `#git-quick-ref` for troubleshooting commands.

---

## Workflow Checklists

### Daily Workflow
- [ ] Pull latest changes before starting
- [ ] Create feature branch from main
- [ ] Make small, focused commits
- [ ] Reference tasks and requirements
- [ ] Push changes regularly
- [ ] Create PR when ready

### Before Committing
- [ ] Tests pass locally
- [ ] No secrets in code
- [ ] Commit message follows format
- [ ] Changes are focused and atomic

### Before Creating PR
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Task marked complete (if applicable)
- [ ] Branch up to date with main
- [ ] Commits squashed if needed

### Before Merging
- [ ] PR approved
- [ ] CI checks pass
- [ ] No merge conflicts
- [ ] Breaking changes documented

---

## Summary

**Key Takeaways:**

1. **Spec-First** - Commit specifications before implementation
2. **Atomic Commits** - One logical change per commit
3. **Traceability** - Reference tasks and requirements always
4. **Clean History** - Meaningful messages, logical ordering
5. **Short Branches** - Keep branches focused and short-lived
6. **Small PRs** - Easier to review, faster to merge
7. **Team Communication** - Coordinate, review promptly, be constructive

**Remember:** Good Git practices make the project history a valuable resource for understanding decisions, debugging issues, and onboarding new developers.

---

## Related Resources

- **Quick Reference:** `.kiro/steering/git-quick-reference.md` (`#git-quick-ref`)
- **Project Structure:** `.kiro/steering/project-structure-guide.md` (`#project-structure`)
- **External:** [Conventional Commits](https://www.conventionalcommits.org/), [Semantic Versioning](https://semver.org/)

---

**Last Updated:** 2025-01-31  
**Version:** 2.0.0 (Streamlined)
