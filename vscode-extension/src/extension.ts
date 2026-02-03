import * as vscode from 'vscode';
import { BackpackCliWrapper } from './backpackCli';
import { BackpackTreeDataProvider } from './backpackTreeDataProvider';
import { BackpackCodeLensProvider } from './backpackCodeLensProvider';

export async function activate(context: vscode.ExtensionContext) {
    console.log('Congratulations, your extension "backpack-vscode" is now active!');

    const workspaceFolder = vscode.workspace.workspaceFolders?.[0].uri.fsPath;
    if (!workspaceFolder) {
        console.log('No workspace folder found.');
    }

    const backpack = new BackpackCliWrapper(workspaceFolder || '.');

    // Tree View
    const treeDataProvider = new BackpackTreeDataProvider(backpack);
    vscode.window.registerTreeDataProvider('backpack-status', treeDataProvider);
    context.subscriptions.push(vscode.commands.registerCommand('backpack.refresh', () => treeDataProvider.refresh()));

    // CodeLens
    context.subscriptions.push(
        vscode.languages.registerCodeLensProvider(
            { language: 'python', scheme: 'file' },
            new BackpackCodeLensProvider(),
        ),
    );

    // Commands
    context.subscriptions.push(
        vscode.commands.registerCommand('backpack.init', () => {
            const terminal = vscode.window.createTerminal('Backpack');
            terminal.show();
            terminal.sendText('backpack init');
        }),
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('backpack.run', (fileUri?: string) => {
            let fileToRun = fileUri;
            if (!fileToRun && vscode.window.activeTextEditor) {
                fileToRun = vscode.window.activeTextEditor.document.uri.fsPath;
            }

            if (!fileToRun) {
                vscode.window.showErrorMessage('No file selected to run.');
                return;
            }

            const terminal = vscode.window.createTerminal('Backpack Run');
            terminal.show();
            terminal.sendText(`backpack run "${fileToRun}"`);
        }),
    );

    // Check version
    try {
        const version = await backpack.getVersion();
        console.log(`Backpack version: ${version}`);
        vscode.window.setStatusBarMessage(`Backpack: ${version}`, 5000);
    } catch (error) {
        console.error(error);
        // Don't show error message immediately on startup to avoid annoyance if not using backpack
        // But maybe a status bar item would be better
    }
}

export function deactivate() {}
