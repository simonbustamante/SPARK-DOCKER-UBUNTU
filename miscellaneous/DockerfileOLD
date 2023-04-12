# Utiliza la imagen oficial de Ubuntu 22.04 como base
FROM ubuntu:22.04

# Actualiza los paquetes de Ubuntu y instala algunas herramientas necesarias
RUN apt-get update && apt-get install -y curl nano python3-pip
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools unixodbc-dev
RUN apt-get install -y unixodbc wget


# Instala Java para Spark
RUN apt-get install -y default-jdk

# Descarga Spark desde el sitio oficial y lo instala
RUN curl -O https://downloads.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz && \
    tar xzf spark-3.3.2-bin-hadoop3.tgz && \
    mv spark-3.3.2-bin-hadoop3 /usr/local/spark && \
    rm spark-3.3.2-bin-hadoop3.tgz

# Descarga e instala Delta Lake
RUN curl -O https://repo1.maven.org/maven2/io/delta/delta-core_2.12/1.1.0/delta-core_2.12-1.1.0.jar && \
    mv delta-core_2.12-1.1.0.jar /usr/local/spark/jars/delta-core_2.12.jar

#RUN curl -O https://downloads.apache.org/hadoop/common/hadoop-3.3.5/hadoop-3.3.5.tar.gz && \
#    tar -xvf hadoop-3.3.5.tar.gz && \
#    mv hadoop-3.3.5 /usr/local/hadoop && \
#    rm hadoop-3.3.5.tar.gz

#ENV HADOOP_HOME /usr/local/hadoop
#ENV PATH $PATH:$HADOOP_HOME/bin


# Instala boto3 con pip
RUN pip3 install boto3
# Instala las librerías necesarias
RUN pip3 install pyodbc pandas datetime argparse boto3 sqlalchemy

# Instala las librerías de DeltaIO
RUN pip3 install delta-spark delta-sharing

# Copia el script validate_data.py al contenedor
COPY uploadParquetToS3.py /app/uploadParquetToS3.py

# Establece la variable de entorno SPARK_HOME
ENV SPARK_HOME=/usr/local/spark

# Establece la variable de entorno PYTHONPATH para utilizar PySpark
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.5-src.zip

# Establece la variable de entorno PATH para incluir spark-submit
ENV PATH=$PATH:$SPARK_HOME/bin

# Ejecuta el script validate_data.py con spark-submit
#CMD ["spark-submit", "/app/uploadParquetToS3.py"]
CMD ["bash"]