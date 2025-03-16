const vscode = require('vscode');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('IssuePilot extension is now active');

    // Register command to configure API keys
    let configureApiKeyCommand = vscode.commands.registerCommand('issuepilot.configureApiKey', async function () {
        const githubToken = await vscode.window.showInputBox({
            prompt: "Enter your GitHub Personal Access Token",
            placeHolder: "Token with 'repo' scope"
        });

        if (githubToken) {
            await vscode.workspace.getConfiguration().update('issuepilot.githubToken', githubToken, true);
            vscode.window.showInformationMessage('GitHub token saved successfully');
        }

        const openaiApiKey = await vscode.window.showInputBox({
            prompt: "Enter your OpenAI API Key",
            placeHolder: "OpenAI API Key"
        });

        if (openaiApiKey) {
            await vscode.workspace.getConfiguration().update('issuepilot.openaiApiKey', openaiApiKey, true);
            vscode.window.showInformationMessage('OpenAI API key saved successfully');
        }
    });

    // Register command to generate GitHub issues
    let generateIssuesCommand = vscode.commands.registerCommand('issuepilot.generateIssues', async function () {
        // Get configuration
        const config = vscode.workspace.getConfiguration('issuepilot');
        const githubToken = config.get('githubToken');
        const openaiApiKey = config.get('openaiApiKey');

        if (!githubToken || !openaiApiKey) {
            vscode.window.showErrorMessage('Please configure your GitHub and OpenAI API keys first.');
            vscode.commands.executeCommand('issuepilot.configureApiKey');
            return;
        }

        // Get repository information
        const username = await vscode.window.showInputBox({
            prompt: "Enter your GitHub username",
            placeHolder: "e.g., octocat"
        });

        if (!username) return;

        const repo = await vscode.window.showInputBox({
            prompt: "Enter your repository name",
            placeHolder: "e.g., my-project"
        });

        if (!repo) return;

        // Get project description for AI-based issue generation
        const projectDescription = await vscode.window.showInputBox({
            prompt: "Describe your project for AI-based issue generation",
            placeHolder: "e.g., A web application for task management using React and Node.js"
        });

        if (!projectDescription) return;

        // Show progress
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Generating GitHub Issues",
            cancellable: true
        }, async (progress, token) => {
            // Create output channel to show results
            const outputChannel = vscode.window.createOutputChannel("IssuePilot");
            outputChannel.show();
            
            try {
                // Call Python script to generate issues
                outputChannel.appendLine("Starting issue generation process...");
                
                // Create a temporary config file
                const tempDir = path.join(context.extensionPath, 'temp');
                if (!fs.existsSync(tempDir)) {
                    fs.mkdirSync(tempDir);
                }
                
                const configFilePath = path.join(tempDir, 'config.json');
                fs.writeFileSync(configFilePath, JSON.stringify({
                    githubToken,
                    openaiApiKey,
                    username,
                    repo,
                    projectDescription
                }));
                
                // Get path to Python script
                const scriptPath = path.join(context.extensionPath, 'src', 'issue_generator.py');
                
                // Run Python script
                const pythonProcess = spawn('python', [scriptPath, configFilePath]);
                
                // Handle script output
                pythonProcess.stdout.on('data', (data) => {
                    outputChannel.appendLine(data.toString());
                });
                
                pythonProcess.stderr.on('data', (data) => {
                    outputChannel.appendLine(`ERROR: ${data.toString()}`);
                });
                
                // Handle process completion
                return new Promise((resolve) => {
                    pythonProcess.on('close', (code) => {
                        if (code === 0) {
                            outputChannel.appendLine("Issues generated successfully!");
                            vscode.window.showInformationMessage("GitHub issues generated successfully!");
                        } else {
                            outputChannel.appendLine(`Process exited with code ${code}`);
                            vscode.window.showErrorMessage("Error generating GitHub issues. Check the output channel for details.");
                        }
                        
                        // Clean up
                        try {
                            fs.unlinkSync(configFilePath);
                        } catch (err) {
                            console.error("Error cleaning up temp file:", err);
                        }
                        
                        resolve();
                    });
                });
            } catch (error) {
                outputChannel.appendLine(`Error: ${error.message}`);
                vscode.window.showErrorMessage(`Error: ${error.message}`);
            }
        });
    });

    context.subscriptions.push(configureApiKeyCommand);
    context.subscriptions.push(generateIssuesCommand);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}; 