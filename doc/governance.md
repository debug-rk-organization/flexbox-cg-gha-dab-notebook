# Governance

## Data Quality Checks:

Data quality is not currently implemented.

#Data Loading:

#Data Schema:

## Unity catalog (if applicable)
### Catalog
* **flexbox_cg_gha_dab_notebook_dev** - dev catalog
* **flexbox_cg_gha_dab_notebook_prod** - prod catalog

### Schemas

* **bronze_flexbox_cg_gha_dab_notebook** - <business use schema>

# Monitoring and Alerts:
Databricks workflow monitoring & alerting

# Testing and Validation:

The pipeline has been tested manually on dev Databricks and breakfix DDAPI.
* Unit tests
* integration tests


# Deployment and CI/CD:

### CI
First block corresponds to the CI (Continuous Integration) and is executed on each **pull request** created on the `main` and `develop` branches. Steps:
* **Test & SonarQube** - Runs unit and integration tests, executes SonarQube static code analisys for code quality verification
* **Gitleaks** - detects hardcoded secrets like passwords, api keys, and tokens
* **Ruff** - checks code formatting

### CD
Next two blocks correspond to the CD (Continuous Deployment) and are executed on each **push** to the `main` and `develop`. Depending on the branch, different configuration is used and the code is deployed to the corresponding environment: main to prod, develop to dev.

Only after all CI steps are succesfull the first deployment step is run, wnich is the `Migrate Schema`. It runs all queries related to Unity Catalog defined in [ddl directory](/flexbox_cg_gha_dab_notebook/bronze_flexbox_cg_gha_dab_notebook/ddl) to set up the database on databricks.

When the `Migrate schema` step is succesfull the last two steps are executed:
* <if ddapi is applicable> `Deploy Workflow Bundle` - deploys the pipeline code as Databricks Asset Bundle, after this step is succesful the pipeline is available in databricks workflows page and scheduled according to the configuration so no further manual steps are needed
