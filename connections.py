from langchain import SQLDatabase

import dotenv
from sshtunnel import SSHTunnelForwarder
#Added following line
from langchain_community.vectorstores.pgvector import PGVector
import psycopg2
import os

dotenv.load_dotenv()


def set_sql_database(customer_code: str, warehouse_id="e9ebcbe4e7edbc39"):
    return SQLDatabase.from_databricks(
        catalog="hive_metastore",
        schema=f"chatbot_{customer_code}",
        warehouse_id=warehouse_id,
        view_support=True,
        include_tables=['items','products','stores','transactions'],
        sample_rows_in_table_info=2,
    )

def set_postgres_conn():
    PG_DATABASE_HOST = os.environ.get("PG_DATABASE_HOST")
    PG_DATABASE_USER = os.environ.get("PG_DATABASE_USER")
    PG_DATABASE_PASSWORD = os.environ.get("PG_DATABASE_PASSWORD")
    PG_DATABASE_NAME = os.environ.get("PG_DATABASE_NAME")

    if os.getenv("ENV_STAGE") not in ["dev", "prd"]:
        ssh_tunnel = SSHTunnelForwarder(
            (os.environ.get("CGP_BASTION_HOST"), 22),
            ssh_username="ubuntu",
            ssh_private_key=os.environ.get("CGP_BASTION_KEY_PATH"),
            remote_bind_address=(PG_DATABASE_HOST, 5432),
        )

        ssh_tunnel.start()

        return psycopg2.connect(
            host="localhost",
            port=ssh_tunnel.local_bind_port,
            user=PG_DATABASE_USER,
            password=PG_DATABASE_PASSWORD,
            dbname=PG_DATABASE_NAME,
        )

    else:
        return psycopg2.connect(
            host=PG_DATABASE_HOST,
            port=5432,
            user=PG_DATABASE_USER,
            password=PG_DATABASE_PASSWORD,
            dbname=PG_DATABASE_NAME,
        )
    
    
def set_postgres_conn_vector():
    PG_DATABASE_HOST = os.environ.get("PG_DATABASE_HOST_VECTOR")
    PG_DATABASE_USER = os.environ.get("PG_DATABASE_USER_VECTOR")
    PG_DATABASE_PASSWORD = os.environ.get("PG_DATABASE_PASSWORD_VECTOR")
    PG_DATABASE_NAME = os.environ.get("PG_DATABASE_NAME_VECTOR")
    PG_DATABASE_DRIVER="psycopg2"


    if os.getenv("ENV_STAGE") not in ["dev", "prd"]:
        ssh_tunnel = SSHTunnelForwarder(
            (os.environ.get("CGP_BASTION_HOST"), 22),
            ssh_username="ubuntu",
            ssh_private_key=os.environ.get("CGP_BASTION_KEY_PATH"),
            remote_bind_address=(PG_DATABASE_HOST, 5432),
        )

        ssh_tunnel.start()

        return PGVector.connection_string_from_db_params(
            host="localhost",
            port=ssh_tunnel.local_bind_port,
            user=PG_DATABASE_USER,
            password=PG_DATABASE_PASSWORD,
            database=PG_DATABASE_NAME,
            driver=PG_DATABASE_DRIVER,

        )

    else:
        return PGVector.connection_string_from_db_params(
            host=PG_DATABASE_HOST,
            port=5432,
            user=PG_DATABASE_USER,
            password=PG_DATABASE_PASSWORD,
            database=PG_DATABASE_NAME,
            driver=PG_DATABASE_DRIVER,
        )
