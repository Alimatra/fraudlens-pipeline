# Connecteurs source

Ce document liste les sources de donnees utilisees dans le pipeline FraudLens et la configuration attendue dans Azure Data Factory.

## Source 1 : Fichiers CSV (dataset PaySim)

- Type : Delimited Text
- Emplacement : conteneur `raw` du compte de stockage
- Format attendu : CSV avec en-tete, encodage UTF-8
- Colonnes cles : `step`, `type`, `amount`, `nameOrig`, `oldbalanceOrg`, `newbalanceOrig`, `nameDest`, `oldbalanceDest`, `newbalanceDest`, `isFraud`, `isFlaggedFraud`

## Source 2 (extension possible) : Base SQL

- Type : Azure SQL Database ou SQL Server on-premise via Self-hosted Integration Runtime
- Usage : simuler une source transactionnelle complementaire (ex. referentiel clients)

## Source 3 (extension possible) : API REST

- Type : REST connector Azure Data Factory
- Usage : simuler un flux de transactions en quasi temps reel (webhook ou polling)

## Linked Services necessaires dans ADF

1. `LS_AzureDataLakeStorage` - connexion au compte ADLS Gen2
2. `LS_AzureDatabricks` - connexion au workspace Databricks (via token ou managed identity)
3. `LS_SourceStorage` - connexion a la source des fichiers bruts (peut etre le meme compte de stockage, conteneur different)

## Datasets ADF necessaires

1. `DS_Source_Transactions` - pointe vers les fichiers CSV source
2. `DS_Raw_Transactions` - pointe vers le conteneur `raw`
