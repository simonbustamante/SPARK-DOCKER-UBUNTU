import os
import json
import boto3
from botocore.exceptions import ClientError
import logging
import datetime
import pyodbc
import sqlalchemy as sql 
import pandas as pd
from delta import *
from delta.tables import *

class DataOps:
    def __init__(
            self,
            INPUT_PATH,
            SCHEMA_PATH,
            args,
            
        ):
        self.INPUT_PATH = INPUT_PATH
        self.SCHEMA_PATH = SCHEMA_PATH
        # Asignar argumentos a variables de instancia
        self.Server = args.Server
        self.UID = args.UID
        self.PASSWORD = args.PASSWORD
        self.DB = args.DB
        self.Query = args.Query
        self.Table = args.Table
        self.Country = args.Country
        self.Route = args.Route
        #self.DateFile = args.TimePeriod
        self.AWSAccessKey = args.AWSAccessKey
        self.AWSSecretKey = args.AWSSecretKey
        self.AWSSessionToken = args.AWSSessionToken
        self.BucketName = args.BucketName
        self.BucketRoute = args.BucketRoute
        self.ChunkSize = args.ChunkSize
        self.Driver = args.Driver
        self.Chunksize = args.ChunkSize
        self.ConnectorType = args.ConnectorType
        self.Port = args.Port  

    def validateData(self, spark):
        # Read input parquet file
        df = spark.read.parquet(self.INPUT_PATH)
        # Leer esquema del archivo parquet a diccionario
        df_schema_dict = json.loads(df.schema.json())
        # Read schema file
        schema_path = os.environ.get("SCHEMA_PATH")
        with open(schema_path) as f:
            schema = f.read()
        # Diccionario del esquema
        schema_dict = json.loads(schema)
        # Convertir los diccionarios a conjuntos de campos
        set1 = {(d['name'], d['type']) for d in schema_dict['fields']}
        set2 = {(d['name'], d['type']) for d in df_schema_dict['fields']}
        if set2.issubset(set1):
            msg = True
        else:
            diff = set1.difference(set2)
            for field in diff:
                msg = f"El campo '{field[0]}' de tipo '{field[1]}' no coincide con el segundo diccionario"
        return msg
          
    def readFromDb(self, spark):
        # Cargar datos de la tabla en un DataFrame de PySpark
        # Ruta del archivo .jar del driver

        if self.ConnectorType == 'sqlserver':
            url = "jdbc:sqlserver://" + self.Server +":"+ self.Port +";databaseName=" + self.DB + ";encrypt=false"
        if self.ConnectorType == 'oracle':
            url =  "jdbc:oracle:thin:@//"+ self.Server +":" + self.Port + "/" + self.DB
        
        if self.Query is None or self.Query == "None":
            df = spark.read \
                .format("jdbc") \
                .option("url", url) \
                .option("dbtable", self.Table) \
                .option("user", self.UID) \
                .option("password", self.PASSWORD) \
                .option("driver", self.Driver) \
                .option("fetchsize", self.ChunkSize)\
                .load()
        else:
            df = spark.read \
                .format("jdbc") \
                .option("url", url) \
                .option("query", self.Query) \
                .option("user", self.UID) \
                .option("password", self.PASSWORD) \
                .option("driver", self.Driver) \
                .option("fetchsize", self.ChunkSize)\
                .load()

        return df
    
    def saveTable(self, DF,MODE):
        now = datetime.datetime.now() # Obtiene la fecha y hora actual
        time = now.strftime("%Y-%m-%d %H:%M:%S") # Formatea la fecha y hora

        froute = self.Route + "/" + self.Country +"/" + self.Table + "/" + time
        if DF is not None and MODE == "overwrite":
            DF.write.mode(MODE)\
                .option("maxRecordsPerFile", self.ChunkSize)\
                .option("compression", "snappy")\
                .parquet(froute)
            msg = "Overwritten on "+froute
        elif DF is not None and MODE == "append":
            DF.write.mode(MODE).parquet(froute)
            msg = "Appended on "+froute
        else:
            msg = "Nothing to change"
        return msg
    
    def saveDeltaTable(self, DF,MODE):
        froute = self.Route + "/" + self.Table
        if DF is not None and MODE == "overwrite":
            DF.repartition(int(DF.count() / 100000) + 1).write.mode(MODE)\
                .option("compression", "snappy")\
                .options(encoding="UTF-8",characterEncoding="UTF-8",overwriteSchema=True)\
                .format('delta')\
                .save(froute)
            msg = "Overwritten on "+froute
        elif DF is not None and MODE == "append" and DF.count() != 0:
            DF.repartition(2).option("maxRecordsPerFile", 4096).write.mode(MODE).options(encoding="UTF-8",characterEncoding="UTF-8",overwriteSchema=True).format('delta').save(froute)
            msg = "Appended on "+froute
        else:
            msg = "Nothing to change"
        return msg
    
    def uploadParquetDirectoryToS3(self,spark):
        """
        Sube todos los archivos Parquet contenidos en el directorio local_dir_path al bucket 
        S3 especificado por bucket_name.
        """
        logger = spark.sparkContext._jvm.org.apache.log4j.LogManager.getLogger(__name__)
        logger.setLevel(spark.sparkContext._jvm.org.apache.log4j.Level.INFO)

        if self.AWSAccessKey is not None and self.AWSSecretKey is not None and self.AWSSessionToken is not None:
            s3 = boto3.client(
                's3',
                aws_access_key_id=self.AWSAccessKey,
                aws_secret_access_key=self.AWSSecretKey,
                aws_session_token=self.AWSSessionToken
            )
        elif self.AWSAccessKey is not None and self.AWSSecretKey is not None:
            s3 = boto3.client(
                's3',
                aws_access_key_id=self.AWSAccessKey,
                aws_secret_access_key=self.AWSSecretKey,
            )
        else:
            s3 = boto3.client('s3')

        now = datetime.datetime.now() # Obtiene la fecha y hora actual
        time = now.strftime("%Y-%m-%d %H:%M:%S") # Formatea la fecha y hora

        # Recorre todos los archivos en el directorio local_dir_path
        for dirpath, dirnames, filenames in os.walk(self.Route+self.Table):
            for filename in filenames:
                if filename.endswith('.parquet'):
                    file_path = os.path.join(dirpath, filename)
                    key = os.path.relpath(file_path, self.Route+self.Table)
                    s3.upload_file(file_path, self.BucketName, self.BucketRoute+self.Country+"/"+self.Table+"/"+time+"/"+key)
                    logger.info('Subiendo '+self.Table+'/'+time+'/'+key)
        logger.info('Fin de la subida de archivos a S3')
