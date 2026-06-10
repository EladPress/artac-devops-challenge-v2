# Connecting to the instance

Instance access is via AWS SSM Session Manager (no SSH, no open port 22). To connect, install the [Session Manager plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html) for the AWS CLI, then run the `ssm_command` shown in the Terraform outputs.
