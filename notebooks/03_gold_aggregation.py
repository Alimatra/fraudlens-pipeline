# Databricks notebook source
# MAGIC %md
# MAGIC # Gold Layer - Agregations et indicateurs metier
# MAGIC
# MAGIC Objectif : produire des tables agregees exploitables pour la detection
# MAGIC de fraude et la restitution analytique (Power BI).

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, sum as spark_sum, when

spark = SparkSession.builder.appName("FraudLens-Gold").getOrCreate()

# COMMAND ----------

STORAGE_ACCOUNT = "REMPLACER_PAR_TON_STORAGE_ACCOUNT"
CONTAINER_SILVER = "silver"
CONTAINER_GOLD = "gold"

silver_path = f"abfss://{CONTAINER_SILVER}@{STORAGE_ACCOUNT}.dfs.core.windows.net/transactions/"
gold_path_summary = f"abfss://{CONTAINER_GOLD}@{STORAGE_ACCOUNT}.dfs.core.windows.net/fraud_summary/"
gold_path_by_type = f"abfss://{CONTAINER_GOLD}@{STORAGE_ACCOUNT}.dfs.core.windows.net/transactions_by_type/"

# COMMAND ----------

df_silver = spark.read.format("delta").load(silver_path)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Indicateur 1 : synthese globale des transactions suspectes

# COMMAND ----------

df_fraud_summary = (
    df_silver
    .groupBy("type")
    .agg(
        count("*").alias("nb_transactions"),
        spark_sum(when(col("isFraud"), 1).otherwise(0)).alias("nb_transactions_suspectes"),
        avg("amount").alias("montant_moyen")
    )
    .withColumn(
        "taux_fraude_pct",
        (col("nb_transactions_suspectes") / col("nb_transactions")) * 100
    )
)

df_fraud_summary.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Indicateur 2 : volume de transactions par type et par periode

# COMMAND ----------

df_by_type = (
    df_silver
    .groupBy("step", "type")
    .agg(
        count("*").alias("nb_transactions"),
        spark_sum("amount").alias("volume_total")
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ecriture des tables Gold

# COMMAND ----------

(
    df_fraud_summary.write
    .format("delta")
    .mode("overwrite")
    .save(gold_path_summary)
)

(
    df_by_type.write
    .format("delta")
    .mode("overwrite")
    .save(gold_path_by_type)
)

print("Agregation Gold terminee avec succes. Tables pretes pour Power BI.")
