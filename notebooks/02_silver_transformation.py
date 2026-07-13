# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Layer - Nettoyage et transformation
# MAGIC
# MAGIC Objectif : nettoyer, typer et dedupliquer les donnees issues de la couche Bronze.

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, when

spark = SparkSession.builder.appName("FraudLens-Silver").getOrCreate()

# COMMAND ----------

STORAGE_ACCOUNT = "REMPLACER_PAR_TON_STORAGE_ACCOUNT"
CONTAINER_BRONZE = "bronze"
CONTAINER_SILVER = "silver"

bronze_path = f"abfss://{CONTAINER_BRONZE}@{STORAGE_ACCOUNT}.dfs.core.windows.net/transactions/"
silver_path = f"abfss://{CONTAINER_SILVER}@{STORAGE_ACCOUNT}.dfs.core.windows.net/transactions/"

# COMMAND ----------

df_bronze = spark.read.format("delta").load(bronze_path)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Nettoyage : typage, deduplication, normalisation

# COMMAND ----------

df_silver = (
    df_bronze
    .dropDuplicates(["nameOrig", "nameDest", "step", "amount"])
    .withColumn("type", upper(trim(col("type"))))
    .withColumn("amount", col("amount").cast("double"))
    .withColumn(
        "isFraud",
        when(col("isFraud") == 1, True).otherwise(False)
    )
    .filter(col("amount") > 0)
    .drop("_source_file")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verification qualite

# COMMAND ----------

nb_lignes_avant = df_bronze.count()
nb_lignes_apres = df_silver.count()
print(f"Lignes avant nettoyage : {nb_lignes_avant}")
print(f"Lignes apres nettoyage : {nb_lignes_apres}")
print(f"Doublons/lignes invalides supprimes : {nb_lignes_avant - nb_lignes_apres}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ecriture en Delta Lake - couche Silver

# COMMAND ----------

(
    df_silver.write
    .format("delta")
    .mode("overwrite")
    .option("mergeSchema", "true")
    .save(silver_path)
)

print("Transformation Silver terminee avec succes.")
