# Azure Declarative Automation Bundle Repository

![Static Badge](https://img.shields.io/badge/CI%2FCD-Automatically_Generated_Template-blue)

## flexbox_cg_gha_dab_notebook

Declarative Automation Bundle project generated with GitHub Actions CI/CD. Edit the bundle definition in `databricks.yml` and the resources under `resources/`; CI validates the bundle and CD deploys it with the Databricks CLI.

## Generated configuration

- Project name: `flexbox_cg_gha_dab_notebook`
- Project environments: `dev,uat,prod`
- Developer workflow: `ui-notebook`
- Compute model: `traditional`
- GitHub administrators team: `flexbox-cg-gha-dab-notebook-admins`
- GitHub developers team: `flexbox-cg-gha-dab-notebook-developers`

`CODEOWNERS` uses the configured team values. The developer workflow and compute model determine the CI build and test steps.

## Repository structure

```
flexbox_cg_gha_dab_notebook/
|-- .github/
|   `-- workflows/              # CI/CD workflows
|-- resources/                  # Databricks resource definitions
|-- databricks.yml              # Declarative Automation Bundle definition
|-- .pre-commit-config.yaml
|-- CODEOWNERS
|-- GitVersion.yml
`-- README.md
```

## CI/CD integration

- GitHub Environments: `dev`, `uat`, `prod`, and `prod_dr` (created for provisioned environments; `prod_dr` is always created)
- Deployment runner: organization runner group `devx-pgi` (`devx-pgi-dr` for `prod_dr`) with label `pg-pgi-4gb-1cpu`
- Shared actions: `procter-gamble/da-pp-pda-github-actions`
- Authentication: GitHub OIDC without an Azure client secret

Repository variables control automatic deployments. Workflows are generated for `dev,uat,prod` regardless of which environments exist today; `CICD_DEPLOY_<ENV>_ENABLED` is `true` only for provisioned environments.

### Repository variables

- `AZURE_TENANT_ID`: Entra tenant shared by all environments
- `CICD_DEPLOY_DEV_ENABLED`: development deployment
- `CICD_DEPLOY_UAT_ENABLED`: UAT deployment
- `CICD_DEPLOY_PROD_ENABLED`: production deployment
- `CICD_DEPLOY_PROD_DR_ENABLED`: production DR deployment

Only the exact lowercase value `true` enables deployment.

### Environment variables

- `AZURE_CLIENT_ID`: client ID of the Entra ID application used by that environment
- `AZURE_SUBSCRIPTION_ID`: Azure subscription ID used for OIDC login
- `WORKSPACE_URL`: target Databricks workspace URL
- `WORKSPACE_CLUSTER_ID`: cluster used to run the test suite
- `SONAR_PROJECT_KEY`: SonarQube project key for the scan

### Secrets

- `SONAR_TOKEN`: SonarQube authentication token

JFrog access for the private package index is obtained through OIDC (via `jfrog/setup-jfrog-cli`), so no JFrog user or token secret is required.

### Federated credentials

Each environment uses a federated credential provisioned on its client service principal. The GitHub environment selects the corresponding `AZURE_CLIENT_ID`, subscription, and workspace values. The authentication configuration is ready to use after provisioning.

Federated credential subject examples:

- Environment: `repo:ORGANIZATION/REPOSITORY:environment:dev`
- Branch: `repo:ORGANIZATION/REPOSITORY:ref:refs/heads/develop`
- Immutable environment: `repo:ORGANIZATION@ORGANIZATION_ID/REPOSITORY@REPOSITORY_ID:environment:dev`

The corresponding identity can deploy the bundle to the target workspace.

## Workflow behavior

- `Pull Request Checks` (`ci-pull-requests.yml`): validates and tests pull requests to `main` or `develop`
- `Continuous Delivery` (`cd.yml`): runs validation once, then deploys only the enabled environments selected for the pushed branch
- `Reusable Validation and Build` (`ci-tasks.yml`): callable workflow used by pull request checks and continuous delivery; it does not run independently
- `Version Tagging` (`util-release-tag.yml`): manually calculates the next version and creates a Git tag and GitHub release; it does not deploy application code

Deployment routing after successful validation:

- Push to `develop`: deploy to `dev` when enabled
- Push to `release/**` or `hotfix/**`: deploy to `uat` when enabled
- Push to `main`: deploy to `prod` and `prod_dr` independently when enabled; both run in parallel

The repository should ideally follow GitFlow: develop features through `feature/**` branches, integrate them into `develop`, stabilize releases through `release/**` or `hotfix/**`, and merge production-ready changes into `main`. Back-merge changes from `main` into `develop` after production or hotfix merges.

### Commit lifecycle

Each push triggers a deployment based on the branch. Pull requests to `develop` or `main` run CI checks. Creating a version is a separate manual step, and a back-merge from `main` into `develop` keeps the branches aligned.

```mermaid
flowchart LR
   feature["feature/**"] -->|PR: CI checks| develop["develop<br/>(deploy dev)"]
   develop --> release["release/** or hotfix/**<br/>(deploy uat)"]
   release -->|PR: CI checks| main["main<br/>(deploy prod + prod_dr)"]
   main --> version["Create version<br/>(manual)"]
   main -.->|back-merge - manual| develop
```

- Merging into `develop` deploys `dev`; pushing `release/**` or `hotfix/**` deploys `uat`; merging into `main` deploys `prod` and `prod_dr` in parallel (each only when its variable is enabled).
- Versioning is manual: `util-release-tag.yml` calculates the next version and creates the tag and release. It does not deploy application code.
- After a production or hotfix merge, back-merge `main` into `develop` so both branches stay in sync.

CD deploys the bundle with the Databricks CLI (`databricks bundle deploy`). No build artifact is stored; the bundle is deployed directly from the checked-out source. GCHM is not used.

`GitVersion.yml` uses Git history. On `main`, it uses `ContinuousDeployment`, increments `Minor`, and ignores version directives in commit messages.

## Maintenance

Actions are pinned to commit SHAs for reproducibility and supply-chain security. Update pins through a reviewed pull request and test CI/CD. Template updates are not synchronized automatically.

Local validation:

`pre-commit run --all-files`

For skipped or queued deployments, check the deployment variable and the `pg-pgi-4gb-1cpu` runners in the `devx-pgi` group (`devx-pgi-dr` for `prod_dr`). For Azure failures, check environment values, the OIDC subject, workspace names, and Azure permissions.
