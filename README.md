# IssuePilot - AI-Powered GitHub Issue Management

IssuePilot is a VSCode extension that uses AI to automate the creation of GitHub issues for your projects. It leverages OpenAI to generate well-structured, contextually relevant issues based on your project description.

## Features

- AI-powered issue generation based on project description
- Automatic creation of issues in your GitHub repository
- Custom label creation and management
- Simple configuration of API keys and repository settings

## Requirements

- Visual Studio Code 1.70.0 or higher
- GitHub account with a personal access token (with 'repo' scope)
- OpenAI API key
- Python 3.6 or higher (automatically used from your environment)

## Installation

### From VS Code Marketplace

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search for "IssuePilot"
4. Click Install

### From GitHub (Development)

1. Clone this repository
2. Make sure you have Node.js and npm installed
3. Run `npm install` in the project folder
4. Run `python -m venv .venv` to create a virtual environment
5. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
6. Install Python dependencies: `pip install requests openai`
7. Open the project in VS Code and press F5 to launch the extension in debug mode

## Usage

1. Open VS Code
2. Configure your API keys via the command palette (Ctrl+Shift+P / Cmd+Shift+P) by typing:
   - `IssuePilot: Configure API Key`
3. Enter your GitHub token and OpenAI API key when prompted
4. Generate issues via the command palette by typing:
   - `IssuePilot: Generate GitHub Issues`
5. Follow the prompts to:
   - Enter your GitHub username
   - Enter your repository name
   - Describe your project for AI-based issue generation
6. The extension will:
   - Generate contextually relevant issues based on your description
   - Create appropriate labels in your repository
   - Create the issues with appropriate titles, descriptions, and labels

## Extension Settings

This extension contributes the following settings:

* `issuepilot.githubToken`: GitHub Personal Access Token with 'repo' scope
* `issuepilot.openaiApiKey`: OpenAI API Key for AI-based issue generation

## Privacy and Security

Your API keys are stored in VS Code's secure storage and are only used for the specified operations. The extension does not collect or transmit any of your personal data beyond what is required to interact with the GitHub and OpenAI APIs.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Enjoy!**
