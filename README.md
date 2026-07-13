# FraudLens Pipeline

Pipeline Data Cloud de bout en bout pour la detection d'anomalies transactionnelles, construit sur Azure avec une architecture Medaillon (Bronze / Silver / Gold).

## Contexte metier

Les organisations financieres traitent des millions de transactions par jour. Detecter les schemas de fraude rapidement, sans ralentir le traitement legitime, est un enjeu critique. Ce projet simule un pipeline capable d'ingerer des flux transactionnels multi-sources, de les nettoyer et enrichir, puis d'exposer des indicateurs exploitables pour la detection d'anomalies.

## Architecture

```
Sources (fichiers CSV, API, SQL)
        |
        v
Azure Data Factory (orchestration + ingestion)
        |
        v
Azure Data Lake Gen2 -- Bronze (donnees brutes)
        |
        v
Azure Databricks (PySpark) -- Silver (nettoyage, typage, deduplication)
        |
        v
Azure Databricks (PySpark) -- Gold (agregations, indicateurs de fraude)
        |
        v
Power BI / exposition analytique
```

Voir `architecture/architecture-diagram.png` pour le schema visuel.

## Stack technique

- Azure Data Lake Storage Gen2
- Azure Data Factory
- Azure Databricks (PySpark)
- Delta Lake (format des tables)
- Python 3.10+
- Power BI (couche de restitution, optionnelle)

## Structure du repo

```
fraudlens-pipeline/
├── README.md
├── architecture/
│   └── architecture-diagram.png
├── ingestion/
│   ├── adf_pipeline_config.json
│   └── source_connectors.md
├── notebooks/
│   ├── 01_bronze_ingestion.py
│   ├── 02_silver_transformation.py
│   └── 03_gold_aggregation.py
├── data_lake/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── requirements.txt
└── .gitignore
```

## Dataset

Ce projet utilise un dataset public de transactions financieres (type PaySim, simulation de transactions mobile money) permettant de reproduire des schemas realistes de fraude : transferts, retraits, paiements, avec un flag `isFraud`.

Source : https://www.kaggle.com/datasets/ealaxi/paysim1

## Pipeline en detail

### 1. Ingestion (Bronze)
Ingestion des fichiers sources bruts dans Azure Data Lake Gen2, sans transformation, avec horodatage et tracabilite de la source. Orchestree par Azure Data Factory.

### 2. Transformation (Silver)
Nettoyage des donnees : typage correct des colonnes, suppression des doublons, gestion des valeurs nulles, normalisation des devises et des types de transaction.

### 3. Agregation (Gold)
Calcul d'indicateurs metier : volume de transactions par type, montant moyen par segment, taux de transactions suspectes, agregations temporelles (par heure/jour) pour alimenter un tableau de bord.

## Indicateurs cles

- Nombre de transactions traitees par lot
- Taux de transactions flaguees comme suspectes
- Distribution des montants par type de transaction
- Latence moyenne du pipeline bronze -> gold

## Comment reproduire

1. Creer un compte Azure (essai gratuit disponible)
2. Provisionner un compte Azure Data Lake Storage Gen2
3. Provisionner un workspace Azure Databricks
4. Importer le dataset PaySim dans un conteneur `raw`
5. Configurer le pipeline Azure Data Factory avec `ingestion/adf_pipeline_config.json` comme reference
6. Executer les notebooks dans l'ordre : `01_bronze_ingestion.py` -> `02_silver_transformation.py` -> `03_gold_aggregation.py`

## Auteur

Alimatou Traore - Data Scientist / AI Specialist
