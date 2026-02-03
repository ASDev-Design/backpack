import * as vscode from 'vscode';

export class BackpackCodeLensProvider implements vscode.CodeLensProvider {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    provideCodeLenses(document: vscode.TextDocument, _token: vscode.CancellationToken): vscode.CodeLens[] {
        const lenses: vscode.CodeLens[] = [];
        const text = document.getText();

        // Regex to find "if __name__ == '__main__':" allowing for some variation
        const regex = /if\s+__name__\s*==\s*['"]__main__['"]\s*:/g;
        let match;

        while ((match = regex.exec(text)) !== null) {
            const range = new vscode.Range(
                document.positionAt(match.index),
                document.positionAt(match.index + match[0].length),
            );

            const cmd: vscode.Command = {
                title: 'Run with Backpack',
                command: 'backpack.run',
                arguments: [document.uri.fsPath],
            };

            lenses.push(new vscode.CodeLens(range, cmd));
        }

        return lenses;
    }
}
