

# DataOps Class

This is a python class that provides a set of methods for data operations such as data validation, reading and writing data to a database, and uploading a directory of parquet files to S3. The class is designed to perform these operations in a flexible and efficient manner by utilizing PySpark, Pandas, and Boto3 libraries.

## Class Methods

The following are the methods in the DataOps class:

### init

The init method initializes the DataOps class with the following input parameters:

 - INPUT_PATH: The path of the input file.

- SCHEMA_PATH: The path of the schema file.

- args: A dictionary that contains the following arguments:

	- Server: The name or IP address of the server.

	- UID: The user ID for the database.

	- PASSWORD: The password for the database.

	- DB: The name of the database.

	- Query: A query string used to extract data from the database.

	- Table: The name of the table in the database.

	- Country: The country code.

	- Route: The local directory path for saving the data.

	- AWSAccessKey: The AWS access key.

	- AWSSecretKey: The AWS secret key.

	- AWSSessionToken: The AWS session token.

	- BucketName: The name of the S3 bucket.

	- BucketRoute: The S3 bucket directory path.

	- ChunkSize: The size of the chunks for reading the data from the database.

	- Driver: The name of the driver for connecting to the database.

	- ConnectorType: The type of database connector (e.g. 'sqlserver' or 'oracle').

	Port: The port number for the database connection.

### validateData

The validateData method takes as input a PySpark SparkSession and returns a message indicating whether the input file schema is a subset of the schema file. If the input file schema is not a subset of the schema file, it returns a message indicating the field that does not match.

  

### readFromDb

The readFromDb method reads data from a database and returns a PySpark DataFrame. The method takes as input a PySpark SparkSession and uses the ConnectorType, Server, Port, DB, Table, UID, PASSWORD, Driver, and ChunkSize attributes of the DataOps class to connect to the database and extract data.

  

### saveTable

The saveTable method saves a PySpark DataFrame to a local directory as a parquet file. The method takes as input a PySpark DataFrame and a string indicating the save mode (i.e. "overwrite" or "append"). The method returns a message indicating the path where the data was saved.

  

### saveDeltaTable

The saveDeltaTable method saves a PySpark DataFrame to a local directory as a Delta table. The method takes as input a PySpark DataFrame and a string indicating the save mode (i.e. "overwrite" or "append"). The method returns a message indicating the path where the data was saved.

  

### uploadParquetDirectoryToS3

The uploadParquetDirectoryToS3 method uploads all parquet files in a local directory to an S3 bucket. The method takes as input a PySpark SparkSession and uses the AWSAccessKey, AWSSecretKey, AWSSessionToken, BucketName, and BucketRoute attributes of the DataOps class

# About .env

The .env file is used to store environment variables that are used by the application. This file is not meant to be committed to source control and should be treated as a configuration file.

The .env file in this case contains the following variables:

-   `AWSAccessKey`: Your AWS access key.
-   `AWSSecretKey`: Your AWS secret key.
-   `AWSSessionToken`: Your AWS session token.
-   `AWS_REGION`: The AWS region where the S3 bucket is located.
-   `INPUT_PATH`: The path to the input directory.
-   `SCHEMA_PATH`: The path to the schema file.
-   `Country`: The country you want to send the data to.
-   `Route`: The local route to create the file.
-   `BucketName`: The name of the S3 bucket.
-   `BucketRoute`: The route in the S3 bucket.
-   `ChunkSize`: The chunk size.
-   `SERVER`: The server name.
-   `UID`: The username for the database connection.
-   `PASSWORD`: The password for the database connection.
-   `DB`: The name of the database.
-   `Query`: The query to execute.
-   `Table`: The name of the table to send the data to.
-   `Port`: The port number for the database connection.
-   `ConnectorType`: The type of connector (e.g. `sqlserver` or `oracle`).
-   `Driver`: The driver for the database connection.
-   `driverClassPath`: The path to the driver class.

Note: Rename this file **EXAMPLE.env** to **.env** before using it.

# About SPARK CLUSTER on docker-compose.yml

This Docker Compose file sets up a cluster of Spark containers, with one container designated as the master node and others as slave nodes. The master node is named "master", the slave nodes are named "slave-1", "slave-2", and "slave-3". The cluster also includes a data store container named "spark-datastore", and a submit container named "submit-1".

The master and slave nodes are built using Dockerfiles located in the "miscellaneous/ubuntu/master" and "miscellaneous/ubuntu/slave" directories, respectively. The data store container is built using a Dockerfile located in the "miscellaneous/ubuntu/datastore" directory. The submit container is built using a Dockerfile located in the "miscellaneous/ubuntu/submit" directory.

The master node is exposed on ports 8080 and 7077. The slave nodes are linked to the master node and share its data volume. The environment variables "SPARK_MASTER_URL", "MASTER_PORT_7077_TCP_ADDR", and "MASTER_PORT_7077_TCP_PORT" are set for each slave node to indicate the URL and address/port of the master node.

The submit-1 container runs the "spark-submit" command to submit a Spark job. The job is defined in the "uploadParquetToS3.py" script, which takes a number of arguments for connecting to a database and uploading data to Amazon S3. The environment variables "AWSAccessKey", "AWSSecretKey", "AWSSessionToken", "AWS_REGION", "INPUT_PATH", and "SCHEMA_PATH" are passed to the container, as well as the arguments for the "uploadParquetToS3.py" script.

The "uploadParquetToS3.py" script is a Python script that uses the PySpark library to read data from a database and write it to Amazon S3 as a Parquet file. The script sets up a Spark session and uses Spark to read data from the database using the Spark DataFrame API. The script then writes the data to Amazon S3 using the Spark "write" method.

The script takes the following command line arguments:

-   Server: the address of the SQL database server
-   UID: the username for connecting to the database
-   PASSWORD: the password for connecting to the database
-   DB: the name of the database
-   Query: an optional SQL query to retrieve data from the database
-   Table: the name of the table to retrieve data from
-   Country: an optional country identifier for the data
-   Route: the local directory where the data will be stored
-   AWSAccessKey: the AWS Access Key for accessing Amazon S3
-   AWSSecretKey: the AWS Secret Access Key for accessing Amazon S3
-   AWSSessionToken: an optional AWS Session Token for accessing Amazon S3
-   BucketName: the name of the Amazon S3 bucket to write data to
-   BucketRoute: an optional route within the bucket to write data to
-   ConnectorType: the type of database connector to use
-   Driver: the name of the JDBC driver to use
-   Port: the port number for connecting to the database
-   ChunkSize: the size of the chunks of data to write to Amazon S3.

## RUN 
 Get inside the source code and run  it

    docker-compose up -d --build

