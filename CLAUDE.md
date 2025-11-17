# CLAUDE.md - AI Assistant Guide

**Last Updated:** 2025-11-17
**Repository:** game-old
**Status:** Initial Development Phase

---

## 📋 Table of Contents

1. [Repository Overview](#repository-overview)
2. [Current State](#current-state)
3. [Development Workflow](#development-workflow)
4. [Codebase Structure](#codebase-structure)
5. [Key Conventions](#key-conventions)
6. [AI Assistant Guidelines](#ai-assistant-guidelines)
7. [Git Workflow](#git-workflow)
8. [Testing Strategy](#testing-strategy)
9. [Future Considerations](#future-considerations)

---

## 🎯 Repository Overview

### Purpose
This repository (`game-old`) appears to be in its initial development phase. It is currently a minimal repository that may be:
- A new game project being set up
- An archived version of a previous game project
- A foundation for future game development

### Technology Stack
**Current:** Not yet established
**To be determined based on development needs**

Common game development stacks to consider:
- **JavaScript/TypeScript:** Phaser, Three.js, PixiJS, Babylon.js
- **Python:** Pygame, Panda3D, Godot (with Python bindings)
- **C#:** Unity, Godot
- **C++:** Unreal Engine, Custom engines
- **Rust:** Bevy, Amethyst
- **Go:** Ebiten, Pixel

---

## 📊 Current State

### Repository Contents
```
game-old/
├── .git/           # Git repository metadata
├── README.md       # Basic project identifier
└── CLAUDE.md       # This file - AI assistant guide
```

### Project Status
- **Initialization:** Complete (initial commit: 3df05e4)
- **Codebase:** Empty - no source files yet
- **Dependencies:** None configured
- **Build System:** Not yet established
- **Testing:** Not yet established

### Active Branch
- Working on: `claude/claude-md-mi3mfhe2rdb4ggme-01AmFFX1GkC1xWaneoPqm3kk`
- Main branch: (to be established)

---

## 🔄 Development Workflow

### Standard Development Process

1. **Planning Phase**
   - Understand the feature/bug requirements
   - Use TodoWrite tool to create task breakdown
   - Identify affected files and systems

2. **Implementation Phase**
   - Write clean, well-documented code
   - Follow established conventions (see below)
   - Test incrementally during development

3. **Review Phase**
   - Run all tests
   - Check code quality and style
   - Verify documentation is updated

4. **Commit Phase**
   - Write clear, descriptive commit messages
   - Follow commit message conventions
   - Push to appropriate branch

### Branch Naming Convention
- Feature branches: `claude/claude-md-<session-id>`
- Always use the branch specified at conversation start
- Never push to unauthorized branches

---

## 📁 Codebase Structure

### Recommended Structure (To Be Established)

When the project develops, consider organizing as follows:

```
game-old/
├── src/                # Source code
│   ├── assets/         # Game assets (sprites, sounds, etc.)
│   ├── components/     # Game components/entities
│   ├── systems/        # Game systems/logic
│   ├── utils/          # Utility functions
│   └── main.*          # Entry point
├── tests/              # Test files
├── docs/               # Documentation
├── config/             # Configuration files
├── build/              # Build output (gitignored)
├── .gitignore          # Git ignore patterns
├── package.json        # Dependencies (if Node.js)
├── README.md           # Project documentation
└── CLAUDE.md           # This file
```

### File Organization Principles

1. **Separation of Concerns:** Keep game logic, rendering, and data separate
2. **Modular Design:** Each file should have a single, clear responsibility
3. **Asset Management:** Keep assets organized by type and purpose
4. **Configuration:** Externalize configuration from code

---

## 🎨 Key Conventions

### Code Style (To Be Established)

**General Principles:**
- Write self-documenting code with clear variable/function names
- Add comments for complex logic or non-obvious decisions
- Keep functions small and focused (single responsibility)
- Avoid deep nesting (max 3-4 levels)

**When established, document:**
- Indentation style (spaces vs tabs, width)
- Naming conventions (camelCase, snake_case, PascalCase)
- File naming patterns
- Comment style and documentation format

### Documentation Standards

1. **Code Comments:**
   - Explain WHY, not WHAT
   - Document complex algorithms
   - Add TODO/FIXME tags for future work

2. **Function Documentation:**
   - Document parameters and return values
   - Include usage examples for complex functions
   - Note any side effects or preconditions

3. **README Updates:**
   - Keep README.md current with setup instructions
   - Document new features and changes
   - Include troubleshooting section

### Security Considerations

- Never commit secrets, API keys, or credentials
- Use environment variables for sensitive configuration
- Validate and sanitize user inputs
- Follow OWASP security best practices
- Be cautious with external dependencies

---

## 🤖 AI Assistant Guidelines

### General Operating Principles

1. **Ask Before Assuming:**
   - Clarify requirements when ambiguous
   - Confirm technology choices before implementing
   - Verify intended behavior for features

2. **Use TodoWrite Tool:**
   - ALWAYS use for multi-step tasks (3+ steps)
   - Keep task list updated in real-time
   - Mark tasks complete immediately after finishing
   - Only one task should be in_progress at a time

3. **Code Quality:**
   - Prefer editing existing files over creating new ones
   - Follow established patterns in the codebase
   - Write tests for new functionality
   - Avoid introducing security vulnerabilities (XSS, injection, etc.)

4. **Communication:**
   - Be concise and direct
   - Use markdown formatting for clarity
   - Include file paths with line numbers when referencing code
   - Don't use emojis unless explicitly requested

### Tool Usage Priorities

1. **File Operations:**
   - Use `Read` instead of `cat`
   - Use `Edit` instead of `sed/awk`
   - Use `Write` for new files (only when necessary)
   - Use `Grep` instead of bash `grep`
   - Use `Glob` instead of `find`

2. **Code Exploration:**
   - Use `Task` tool with `subagent_type=Explore` for broad codebase exploration
   - Use direct search tools only for specific queries

3. **Parallel Execution:**
   - Run independent operations in parallel
   - Use sequential execution only when operations depend on each other

### When Working on This Repository

1. **First Steps:**
   - Read this CLAUDE.md file first
   - Check README.md for project-specific info
   - Understand current project structure before making changes

2. **Before Adding Dependencies:**
   - Confirm with user if it's a new project without package manager
   - Choose dependencies that align with project goals
   - Consider bundle size and maintenance status

3. **Before Major Architectural Decisions:**
   - Discuss options with the user
   - Consider scalability and maintainability
   - Document the rationale for choices

---

## 🔀 Git Workflow

### Commit Message Format

```
<type>: <subject>

<body (optional)>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring (no feature change)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependency updates
- `perf`: Performance improvements

**Examples:**
```
feat: add player movement system

Implement basic WASD movement controls with velocity and collision detection.

fix: correct sprite rendering offset

The player sprite was rendering 10px too low due to incorrect anchor point calculation.
```

### Git Commands

**Committing:**
```bash
git add <files>
git commit -m "$(cat <<'EOF'
<commit message here>
EOF
)"
```

**Pushing:**
```bash
git push -u origin <branch-name>
```
- Always use the branch specified at conversation start
- Retry up to 4 times on network errors (exponential backoff: 2s, 4s, 8s, 16s)

**Never:**
- Force push to main/master
- Amend commits from other developers
- Skip hooks without explicit user request

---

## 🧪 Testing Strategy

### To Be Established

When implementing tests, consider:

1. **Unit Tests:**
   - Test individual functions and components
   - Mock external dependencies
   - Aim for high coverage of critical paths

2. **Integration Tests:**
   - Test component interactions
   - Verify game systems work together
   - Test asset loading and management

3. **Test Organization:**
   - Mirror source code structure in test directory
   - Name test files clearly (e.g., `player.test.js`)
   - Group related tests using describe blocks

4. **Running Tests:**
   - Document how to run tests in README
   - Set up CI/CD for automated testing (optional)
   - Include tests in development workflow

---

## 🚀 Future Considerations

### Areas to Document as Project Grows

1. **Game Architecture:**
   - Entity-Component-System (ECS) pattern?
   - Game loop implementation
   - State management approach
   - Rendering pipeline

2. **Asset Pipeline:**
   - Asset creation and export workflow
   - Optimization strategies
   - Loading and caching mechanisms

3. **Performance:**
   - Frame rate targets
   - Profiling tools and methods
   - Optimization guidelines

4. **Build and Deployment:**
   - Build scripts and processes
   - Deployment targets (web, desktop, mobile)
   - Versioning strategy

5. **Collaboration:**
   - Code review process
   - Design documentation
   - Communication channels

---

## 📝 Maintenance

### Updating This Document

This CLAUDE.md file should be updated when:
- Project structure changes significantly
- New conventions are established
- Technology stack is chosen or updated
- New tools or workflows are introduced
- Common patterns or anti-patterns are identified

### Version History

- **2025-11-17:** Initial creation - documented empty repository state and established foundational guidelines

---

## 🎮 Game-Specific Notes

### To Be Added

As the game develops, document:
- Game genre and mechanics
- Target platform(s)
- Performance requirements
- Art style and asset requirements
- Audio requirements
- Control schemes
- Multiplayer considerations (if applicable)

---

**For questions or clarifications about this guide, please ask during the development session.**
