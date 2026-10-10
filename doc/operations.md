# Operations

## Key Contacts
* Product Owner:
* Dev team(L3 support):

## Azure Resources Used
### Dev
* Databricks workspace: `adb-1111111111111110.10.azuredatabricks.net`
* Azure Subscription:
* Azure Resource group:
* Azure storage account:
* Azure storage container:
* service principal: az-sp-chk-01-dev
* Azure Key Vault: kv-chk-dev-01-scope
### Prod
* Databricks workspace: `adb-1111111111111112.12.azuredatabricks.net`
* Azure Subscription:
* Azure Resource group:
* Azure storage account:
* Azure storage container:
* service principal: az-sp-chk-01-prod
* Azure Key Vault: kv-chk-prod-01-scope

## Regularly Scheduled Maintenance
### Changing passwords/tokens
If the password/token expires, please create a new one and upload it in Azure KeyVault.
> Note that there are no pipeline-speciffic secrets for this application.

## Common Problems & Solutions
### Fail scenario
After workflow failure an email is sent to the defined group(s). The list of emails addresses is set up in the databricks asset bundle [job definition](/resources/flexbox_cg_gha_dab_notebook_job.yml) There is no need to remove any data before the restart. You can simply rerun the process from where it failed.

For CDL publication issues contact DDAPI support (applies only to `publish_task` of the pipeline).
