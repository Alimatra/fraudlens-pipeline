# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Layer - Ingestion brute
# MAGIC
# MAGIC Objectif : ingerer les fichiers sources bruts dans le Data Lake Gen2,
# MAGIC sans transformation metier, avec ajout de metadonnees de tracabilite.

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name, lit

spark = SparkSession.builder.appName("FraudLens-Bronze").getOrCreate()

# COMMAND ----------

# Parametres - a adapter selon ton compte de stockage
STORAGE_ACCOUNT = "REMPLACER_PAR_TON_STORAGE_ACCOUNT"
CONTAINER_RAW = "raw"
CONTAINER_BRONZE = "bronze"

raw_path = f"abfss://{CONTAINER_RAW}@{STORAGE_ACCOUNT}.dfs.core.windows.net/transactions/"
bronze_path = f"abfss://{CONTAINER_BRONZE}@{STORAGE_ACCOUNT}.dfs.core.windows.net/transactions/"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lecture du dataset source (format CSV - ex. PaySim)

# COMMAND ----------

df_raw = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(raw_path)
)

print(f"Nombre de lignes ingerees : {df_raw.count()}")
df_raw.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ajout des metadonnees de tracabilite

# COMMAND ----------

df_bronze = (
    df_raw
    .withColumn("_ingestion_timestamp", current_timestamp())
    .withColumn("_source_file", input_file_name())
    .withColumn("_layer", lit("bronze"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ecriture en Delta Lake - couche Bronze

# COMMAND ----------

(
    df_bronze.write
    .format("delta")
    .mode("append")
    .save(bronze_path)
)

print("Ingestion Bronze terminee avec succes.")
