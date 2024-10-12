import os
import pandas as pd
import psycopg2
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

###############################################
# Parameters
###############################################
csv_file = "valorant-game\data\data_clean.csv"
postgres_host = "postgres"  # Replace with your PostgreSQL host
postgres_db = "airflow"
postgres_user = "airflow"
postgres_password  = "airflow"
now = datetime.now()

###############################################
# Function to upload data to PostgreSQL
###############################################
def upload_to_postgres():
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Create a connection to PostgreSQL
    conn = psycopg2.connect(
        host=postgres_host,
        database=postgres_db,
        user=postgres_user,
        password=postgres_password
    )
    
    # Create a cursor object
    cursor = conn.cursor()

    for index, row in df.iterrows():
        try:
            # Print the current row for debugging
            print(f"Inserting Row {index}: {row.values}")
            cursor.execute(
                """
                INSERT INTO your_table_name (
                    Agent, Role, Score, Trend, "Win %", "Pick %", "Dmg/Round", KDA, Map, 
                    "Play %", "Attacker Win %", "Attacker KDA", "Defender Win %", 
                    "Defender KDA", "Best Site", "A Pick %", "A Defuse %", "B Pick %", 
                    "B Defuse %", "C Pick %", "C Defuse %"
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                tuple(row)  # Convert row to tuple for SQL insertion
            )
        except Exception as e:
            print(f"Error inserting row {index}: {e}")  # Print the error message
            continue  # Skip to the next row in case of error
    
    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
    print("Data uploaded successfully to PostgreSQL.")

###############################################
# DAG Definition
###############################################
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),  # Set a fixed start date
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

# Daily run schedule: Every day at midnight
dag = DAG(
    dag_id="upload_valo_data_to_postgres",
    description="Upload data from CSV to PostgreSQL.",
    default_args=default_args,
    schedule_interval="0 0 * * *"  # Every day at midnight
)

###############################################
# Task Definitions
###############################################
# Start and End tasks
start = DummyOperator(task_id="start", dag=dag)
end = DummyOperator(task_id="end", dag=dag)

# Upload data to PostgreSQL task
upload_task = PythonOperator(
    task_id="upload_to_postgres",
    python_callable=upload_to_postgres,
    dag=dag
)

# Task Dependencies
start >> upload_task >> end
