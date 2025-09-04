# PyModbus Dependency Monitoring

This repository includes automated monitoring of the PyModbus dependency in Home Assistant Core to ensure compatibility and timely updates.

## How it works

The monitoring system consists of:

1. **GitHub Action Workflow** (`.github/workflows/monitor-pymodbus.yaml`)
   - Runs last day of the month
   - Can be manually triggered via GitHub Actions UI
   - Fetches the latest `requirements_all.txt` from Home Assistant Core
   - Extracts the current PyModbus version
   - Compares with the last known version

2. **Version Tracking** (Hardcoded in Workflow)
   - Last known PyModbus version is hardcoded in the workflow file
   - Must be manually updated when PyModbus is updated in Home Assistant Core
   - Simple and transparent approach

3. **Automated Notifications**
   - Creates GitHub issues when PyModbus version changes
   - Issues are labeled with `pymodbus-update`, `dependencies`, and `automated`
   - Prevents duplicate issues for the same version

## What happens when a version change is detected

1. **Issue Creation**: A new GitHub issue is created with:
   - Clear title indicating the version change
   - Detailed description with old and new versions
   - Checklist of recommended next steps
   - Link to the Home Assistant requirements file

2. **Manual Update Required**: The hardcoded version in the workflow must be updated

3. **Summary**: A workflow summary is generated showing the monitoring results

## Manual Actions

### Triggering the Workflow
You can manually trigger the monitoring workflow by:
1. Going to the "Actions" tab in GitHub
2. Selecting "Monitor PyModbus Dependency"
3. Clicking "Run workflow"

### Updating the Tracked Version
When PyModbus is updated in Home Assistant Core:
1. Open `.github/workflows/monitor-pymodbus.yaml`
2. Update the `LAST_KNOWN_PYMODBUS_VERSION` environment variable
3. Commit and push the changes
4. The workflow will now track the new version

## Monitoring Home Assistant Core

The workflow monitors: https://github.com/home-assistant/core/blob/dev/requirements_all.txt

This ensures we're always aware of PyModbus updates in the main Home Assistant repository, allowing for proactive testing and compatibility verification.

## Issue Labels

Issues created by this workflow are automatically labeled with:
- `pymodbus-update`: Indicates this is a PyModbus version update
- `dependencies`: Categorizes as a dependency-related issue
- `automated`: Shows this was created by automation

## Troubleshooting

If the workflow fails:
1. Check the workflow logs in the Actions tab
2. Verify the Home Assistant Core repository is accessible
3. Ensure the workflow has proper permissions to create issues
4. Check if PyModbus is still present in the requirements file
