# Plan: Backpack VS Code Extension

## Overview

The **Backpack VS Code Extension** will provide a seamless interface for managing AI agents, credentials, and configurations directly within the editor. It aims to make the "invisible" parts of Backpack (encrypted state, keychain access) visible and manageable.

## Goals
1.  **Visual Management**: View and edit `agent.lock` layers without manual CLI commands.
2.  **One-Click Run**: Execute agents with automatic JIT injection handling in the integrated terminal.
3.  **Credential Management**: Add/Remove keys from the secure vault via a GUI.
4.  **Template Scaffolding**: Create new agents from templates using a wizard.

## Feature Roadmap

### Phase 1: MVP (Minimum Viable Product)
*   **Agent Status View**: A sidebar view showing the current `agent.lock` status (Size, Layers, Required Keys).
*   **Command Palette Integration**:
    *   `Backpack: Init`
    *   `Backpack: Run`
    *   `Backpack: Add Key`
    *   `Backpack: List Keys`
*   **Run Lens**: A "Run with Backpack" CodeLens above `if __name__ == "__main__":` in Python files.

### Phase 2: Visual Editors
*   **Agent Lock Editor**: A custom editor for `agent.lock` files that allows:
    *   Viewing required credentials (and adding them if missing).
    *   Editing the "Personality" layer (System Prompt) in a rich text area.
    *   Viewing Memory stats.
*   **Keychain Manager**: A panel to view available keys in the vault (names only, never values) and add new ones.

### Phase 3: Advanced Integration
*   **Template Wizard**: A GUI for `backpack template use` to browse and preview templates.
*   **Memory Inspector**: View and modify the ephemeral memory layer (for debugging).
*   **Export/Import GUI**: Drag-and-drop export/import of agents.

## Technical Architecture

### 1. Extension Structure
*   **Language**: TypeScript
*   **Framework**: VS Code Extension API
*   **Communication**: Spawns the `backpack` CLI for all heavy lifting. This ensures the extension doesn't need to re-implement encryption logic and stays in sync with the core tool.

### 2. Key Components
*   `BackpackCliWrapper`: A TypeScript class to execute `backpack` commands and parse JSON output.
    *   *Requirement*: Add `--json` output flag to `backpack` CLI commands (Future Task).
*   `AgentLockProvider`: A `CustomTextEditorProvider` for `agent.lock` files.
*   `BackpackTreeDataProvider`: Populates the "Backpack" view in the Activity Bar.

### 3. JIT Injection Handling
*   The extension will not handle encryption directly.
*   When "Running" an agent, it will create a new VS Code Terminal and send the `backpack run agent.py` command string. This allows the CLI's interactive prompt ("Allow access to key?") to work naturally in the terminal.

## Implementation Steps

### Step 1: Setup
1.  Initialize project with `yo code`.
2.  Set up ESLint, Prettier, and TypeScript configuration.

### Step 2: CLI Wrapper
1.  Implement a wrapper to call `backpack version` to verify installation.
2.  Implement `backpack status` parsing (may need to parse text output until JSON support is added).

### Step 3: Commands & Tree View
1.  Create a "Backpack" view container.
2.  Add a TreeView showing:
    *   Current Agent (if `agent.lock` exists)
    *   Required Keys
    *   Personality
3.  Register commands (`backpack.init`, `backpack.run`).

### Step 4: CodeLens
1.  Implement `CodeLensProvider` for Python files.
2.  Detect `main` blocks and add "Run with Backpack".

### Step 5: Packaging
1.  Use `vsce` to package the extension.
2.  Publish to VS Code Marketplace.

## Requirements
*   **Backpack CLI** installed (`pip install backpack`).
*   **Python** extension for VS Code (optional but recommended).

## Open Questions
*   Should we bundle the python package or rely on the user's environment?
    *   *Decision*: Rely on user's environment to ensure we use the same vault/keychain context.
*   How to handle multiple workspaces?
    *   *Decision*: Each workspace folder is treated as a potential agent root.
