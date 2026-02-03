import * as vscode from 'vscode';
import * as path from 'path';
import { BackpackCliWrapper } from './backpackCli';

export class BackpackTreeDataProvider implements vscode.TreeDataProvider<BackpackTreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<BackpackTreeItem | undefined | null | void> =
        new vscode.EventEmitter<BackpackTreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<BackpackTreeItem | undefined | null | void> =
        this._onDidChangeTreeData.event;

    constructor(private backpack: BackpackCliWrapper) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: BackpackTreeItem): vscode.TreeItem {
        return element;
    }

    async getChildren(element?: BackpackTreeItem): Promise<BackpackTreeItem[]> {
        if (!element) {
            // Root items
            try {
                const status = await this.backpack.getStatus();
                if (status.error) {
                    if (status.error.includes('No agent.lock')) {
                        return [
                            new BackpackTreeItem('No Agent Found', vscode.TreeItemCollapsibleState.None, {
                                iconPath: new vscode.ThemeIcon('info'),
                                description: 'Run "Backpack: Init" to create one',
                            }),
                        ];
                    }
                    return [
                        new BackpackTreeItem('Error', vscode.TreeItemCollapsibleState.None, {
                            description: status.error,
                            iconPath: new vscode.ThemeIcon('error'),
                        }),
                    ];
                }

                const items: BackpackTreeItem[] = [];

                // Agent Info
                items.push(
                    new BackpackTreeItem('Agent', vscode.TreeItemCollapsibleState.Expanded, {
                        description: path.basename(status.file_path),
                        iconPath: new vscode.ThemeIcon('hubot'),
                    }),
                );

                // Credentials
                const creds = status.layers.credentials;
                items.push(
                    new BackpackTreeItem(`Credentials`, vscode.TreeItemCollapsibleState.Collapsed, {
                        description: `${creds.length} keys`,
                        iconPath: new vscode.ThemeIcon('key'),
                        contextValue: 'credentials',
                        data: creds,
                    }),
                );

                // Personality
                items.push(
                    new BackpackTreeItem('Personality', vscode.TreeItemCollapsibleState.None, {
                        iconPath: new vscode.ThemeIcon('person'),
                        command: {
                            command: 'backpack.editPersonality',
                            title: 'Edit Personality',
                            arguments: [],
                        },
                    }),
                );

                return items;
            } catch (e: unknown) {
                const message = e instanceof Error ? e.message : String(e);
                return [
                    new BackpackTreeItem('Error loading status', vscode.TreeItemCollapsibleState.None, {
                        description: message,
                        iconPath: new vscode.ThemeIcon('error'),
                    }),
                ];
            }
        } else if (element.contextValue === 'credentials') {
            const creds = element.data as string[];
            if (creds.length === 0) {
                return [new BackpackTreeItem('No credentials defined', vscode.TreeItemCollapsibleState.None)];
            }
            return creds.map(
                (c) =>
                    new BackpackTreeItem(c, vscode.TreeItemCollapsibleState.None, {
                        iconPath: new vscode.ThemeIcon('key'),
                    }),
            );
        }

        return [];
    }
}

export class BackpackTreeItem extends vscode.TreeItem {
    public data: unknown;

    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        options?: {
            iconPath?: vscode.ThemeIcon | vscode.Uri | { light: vscode.Uri; dark: vscode.Uri };
            description?: string;
            contextValue?: string;
            command?: vscode.Command;
            data?: unknown;
        },
    ) {
        super(label, collapsibleState);
        if (options) {
            this.iconPath = options.iconPath;
            this.description = options.description;
            this.contextValue = options.contextValue;
            this.command = options.command;
            this.data = options.data;
        }
    }
}
