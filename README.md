# CloudFormation Graph

## Installation
Requires python3

- `python setup.py install`

## Usage
You probably want to install dot / graphviz to turn the output into images.

### Change Sets
```bash
# With the AWS CLI
aws cloudformation describe-change-set --change-set-name $cs_name | cfn-graph | dot -Tpng > output.png

# When copying from the console
echo $copied_from_console | cfn-graph --wrap changeset --console | dot -Tpng > output.png
```

