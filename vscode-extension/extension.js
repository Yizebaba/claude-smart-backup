const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');
const os = require('os');

let statusBarItem;
let monitorProcess;

function activate(context) {
    console.log('AI Chat Backup extension is now active');

    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = "$(database) AI Backup";
    statusBarItem.tooltip = "AI Chat Backup Status";
    statusBarItem.command = 'ai-chat-backup.status';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('ai-chat-backup.backup', backupNow),
        vscode.commands.registerCommand('ai-chat-backup.restore', restoreLatest),
        vscode.commands.registerCommand('ai-chat-backup.status', showStatus),
        vscode.commands.registerCommand('ai-chat-backup.configure', configure)
    );

    // Start monitoring if enabled
    const config = vscode.workspace.getConfiguration('aiChatBackup');
    if (config.get('enabled')) {
        startMonitoring();
    }
}

function backupNow() {
    const scriptPath = getScriptPath();
    exec(`python3 "${scriptPath}" --check`, (error, stdout, stderr) => {
        if (error) {
            vscode.window.showErrorMessage(`Backup failed: ${error.message}`);
            return;
        }
        vscode.window.showInformationMessage('✅ Backup completed successfully');
        updateStatusBar('✅');
    });
}

function restoreLatest() {
    vscode.window.showWarningMessage(
        'Restore latest backup? This will overwrite current data.',
        'Yes', 'No'
    ).then(selection => {
        if (selection === 'Yes') {
            const scriptPath = getScriptPath();
            exec(`python3 "${scriptPath}" --restore`, (error, stdout, stderr) => {
                if (error) {
                    vscode.window.showErrorMessage(`Restore failed: ${error.message}`);
                    return;
                }
                vscode.window.showInformationMessage('✅ Restore completed successfully');
            });
        }
    });
}

function showStatus() {
    const scriptPath = getScriptPath();
    exec(`python3 "${scriptPath}" --status`, (error, stdout, stderr) => {
        if (error) {
            vscode.window.showErrorMessage(`Failed to get status: ${error.message}`);
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            'aiBackupStatus',
            'AI Chat Backup Status',
            vscode.ViewColumn.One,

        );

        panel.webview.html = getStatusHtml(stdout);
    });
}

function configure() {
    vscode.commands.executeCommand('workbench.action.openSettings', 'aiChatBackup');
}

function startMonitoring() {
    const scriptPath = getScriptPath();
    monitorProcess = exec(`python3 "${scriptPath}" --daemon`);

    monitorProcess.stdout.on('data', (data) => {
        console.log(`Monitor: ${data}`);
        if (data.includes('✅ 备份成功')) {
            updateStatusBar('✅');
        }
    });
}

function updateStatusBar(icon) {
    statusBarItem.text = `$(database) ${icon}`;
    setTimeout(() => {
        statusBarItem.text = "$(database) AI Backup";
    }, 3000);
}

function getScriptPath() {
    const extensionPath = __dirname;
    return path.join(extensionPath, '..', 'monitor.py');
}

function getStatusHtml(status) {
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { padding: 20px; font-family: sans-serif; }
                pre { background: #f5f5f5; padding: 15px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h2>📊 AI Chat Backup Status</h2>
            <pre>${status}</pre>
        </body>
        </html>
    `;
}

function deactivate() {
    if (monitorProcess) {
        monitorProcess.kill();
    }
}

module.exports = {
    activate,
    deactivate
};
