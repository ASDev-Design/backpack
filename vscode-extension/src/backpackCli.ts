import * as cp from 'child_process';

export interface BackpackStatus {
    file_path: string;
    size: number;
    layers: {
        credentials: string[];
        personality: Record<string, string>;
        memory: Record<string, unknown>;
        deployment: Record<string, unknown>;
    };
    error?: string;
}

export class BackpackCliWrapper {
    private cwd: string;

    constructor(cwd: string) {
        this.cwd = cwd;
    }

    public async getVersion(): Promise<string> {
        try {
            const output = await this.execute('version');
            return output;
        } catch {
            throw new Error('Backpack CLI not found or not working. Make sure "backpack" is in your PATH.');
        }
    }

    public async getStatus(): Promise<BackpackStatus> {
        const output = await this.execute('status --json');
        return JSON.parse(output);
    }

    private execute(args: string): Promise<string> {
        return new Promise((resolve, reject) => {
            cp.exec(`backpack ${args}`, { cwd: this.cwd }, (err, stdout, stderr) => {
                if (err) {
                    reject(stderr || err.message);
                } else {
                    resolve(stdout.trim());
                }
            });
        });
    }
}
