# Python Azure Function

1. Create Azure Resource Group
`az group create --name "$GROUP" --location "$REGION"`

2. Deploy all resouces
`az deployment group create -n "$GROUP" -g "$GROUP" --template-file azuredeploy_paf.json`
