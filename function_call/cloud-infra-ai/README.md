# Cloud Infra AI

Function call example with Claude 3 sonnet. It reads a terraform plan and, if AMI changes are found, list the differences from the release notes in amazon-ecs-ami github repo.

## Usage

```
% python main.py eval --help
Usage: main.py eval [OPTIONS]

Options:
  --terraform-plan TEXT  Terraform json plan file path  [required]
  --help                 Show this message and exit.

```

To generate a terraform plan in json, execute the following commands:

```
terraform plan -out=./plan/out.txt
terraform show -json ./plan/out.json
```