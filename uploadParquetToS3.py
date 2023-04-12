import argparse
import os
from DataOps import DataOps
from pyspark.sql import SparkSession

parser = argparse.ArgumentParser(description='Conexion SQL Phyton, suma/resta/multiplica a y b')
parser.add_argument('-S', '--Server', type=str, required=True, help='Server de Base de Datos SQL')
parser.add_argument('-U', '--UID', type=str, required=True, help='usuario Conexion')
parser.add_argument('-P', '--PASSWORD', type=str, required=True, help='Password Conexion')
parser.add_argument('-DB', '--DB', type=str, required=True, help='Nombre de Base de datos')
#parser.add_argument('-X', '--XConection', type=str, choices=['Y','N'], default= 'N',required=False, help='parametro para identificar si es conexion por usuario windows o por usuario SQL')
parser.add_argument('-Q', '--Query', type=str, required=False, help='Query a Ejecutar')
parser.add_argument('-T', '--Table', type=str, required=True, help='Tabla a enviar')
parser.add_argument('-C', '--Country', type=str, required=False, help='Pais a Enviar')
parser.add_argument('-R', '--Route', type=str, required=True, help='Ruta Local Para crear archivo')
#parser.add_argument('-PE', '--TimePeriod', type=str, required=False, help='periodo del archivo')
parser.add_argument('-AA', '--AWSAccessKey', type=str, required=True, help='AWS ACCESS KEY')
parser.add_argument('-AS', '--AWSSecretKey', type=str, required=True, help='AWS SECRET ACCESS KEY')
parser.add_argument('-TK', '--AWSSessionToken', type=str, required=False, help='AWS SESSION TOKEN')
parser.add_argument('-B', '--BucketName', type=str, required=True, help='Nombre Bucket')
parser.add_argument('-BR', '--BucketRoute', type=str, required=False, help='Ruta Bucket')
parser.add_argument('-CT', '--ConnectorType', type=str, required=True, help='Tipo de Conector')
parser.add_argument('-DR', '--Driver', type=str, required=True, help='Driver de Base de Datos')
parser.add_argument('-PO', '--Port', type=str, required=True, help='Puerto de Base de Datos')
parser.add_argument('-CS', '--ChunkSize', type=int, required=True, help='Chunk Size')
args = parser.parse_args()

# Instance object
DataOps = DataOps(
        os.environ.get("INPUT_PATH"),
        os.environ.get("SCHEMA_PATH"),
        args
    )

# Initialize SparkSession
if DataOps.AWSSessionToken is not None:
    spark = SparkSession.builder.appName("From DB to S3")\
        .config("spark.hadoop.fs.s3a.access.key", DataOps.AWSAccessKey) \
        .config("spark.hadoop.fs.s3a.secret.key", DataOps.AWSSecretKey) \
        .config("spark.hadoop.fs.s3a.session.token", DataOps.AWSSessionToken)\
        .getOrCreate()
else:
    spark = SparkSession.builder.appName("From DB to S3")\
        .config("spark.hadoop.fs.s3a.access.key", DataOps.AWSAccessKey) \
        .config("spark.hadoop.fs.s3a.secret.key", DataOps.AWSSecretKey) \
        .getOrCreate()

# Validate Data
#msg = DataOps.validateData(spark)
os.makedirs(DataOps.Route,exist_ok=True)
df = DataOps.readFromDb(spark)
DataOps.saveTable(df,"overwrite")
#DataOps.uploadParquetDirectoryToS3(spark)


