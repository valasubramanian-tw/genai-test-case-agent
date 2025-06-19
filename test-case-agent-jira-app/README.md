# Forge Hello World

This project contains a Forge app written in JavaScript that generates test cases for a given Jira issue.

See [developer.atlassian.com/platform/forge/](https://developer.atlassian.com/platform/forge) for documentation and tutorials explaining Forge.

## Requirements

- [Node.js](https://nodejs.org/) (version 14 or 16 recommended)
- [Forge CLI](https://developer.atlassian.com/platform/forge/cli-reference/) (`npm install -g @forge/cli`)
- Atlassian account and Jira Cloud instance

See [Set up Forge](https://developer.atlassian.com/platform/forge/set-up-forge/) for detailed setup instructions.

## Quick start

1. **Install top-level dependencies:**
   ```sh
   npm install
   ```

2. **Install dependencies inside the `static/hello-world` directory:**
   ```sh
   cd static/hello-world
   npm install
   ```

3. **Modify your app by editing files in `static/hello-world/src/`.**

4. **Build your app (inside the `static/hello-world` directory):**
   ```sh
   npm run build
   ```

5. **Deploy your app:**
   ```sh
   cd ../..
   forge deploy
   ```

6. **Install your app in an Atlassian site:**
   ```sh
   forge install
   # For upgrades:
   forge install --upgrade
   ```

7. **Start the development tunnel (for local development):**
   ```sh
   forge tunnel
   ```

### Notes

- Use the `forge deploy` command to persist code changes.
- Use the `forge install` command to install the app on a new site.
- Once the app is installed on a site, new app changes are picked up after deployment without needing to rerun the install command.

## Support

See [Get help](https://developer.atlassian.com/platform/forge/get-help/) for support and feedback.
