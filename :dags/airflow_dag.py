import pandas as pd
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.python import BranchPythonOperator
from airflow.sdk import Variable


from api_call_script import api_call
from candidate_screening_script import screen_candidates
from schedule_candidates_script import schedule_candidates
from feedback_status_script import feedback_status
from onboard_candidates_script import onboard_candidates


# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'admin',
    # ensures next task doesn't run till the previous task has completed
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
    'execution_timeout': timedelta(seconds=30) 
}

# function to download the interviewer file from S3
def mock_interviewer_data(local_path):
    import pandas as pd
    import logging
    logging.info("Bypassing AWS S3 and generating local mock interviewer data...")
    
    # Generate fake interviewers
    mock_data = {
        "Interviewer_Name": ["John Doe", "Jane Smith", "Alan Turing", "Grace Hopper"],
        "Department": ["Engineering", "Sales", "Management", "HR"],
        "interviewer_email": ["john@example.com", "jane@example.com", "alan@example.com", "grace@example.com"]
    }
    
    df = pd.DataFrame(mock_data)
    file_path = f"{local_path}/interviewer_list.csv"
    df.to_csv(file_path, index=False)
    
    logging.info(f"Success! Mock interviewer list saved to {file_path}")
    return file_path	

# DAG
project_dag = DAG(
            'airflow_course_dag',
            default_args=default_args,
            description='Project DAG',
            schedule= "*/3 * * * *",
            catchup=False
        )

# task to get data from API
fallback_dir = "/Users/vineethyadav/airflow/dags"

task1 = PythonOperator(
                    task_id='api_data_fetch',
                    python_callable = api_call,
                    op_kwargs = {
                        'base_dir': Variable.get("base_dir_var", default="./dags")
                                },
                    dag=project_dag
            )

# task to perform initial screening of candidate profiles            
task2 = PythonOperator(
			task_id = 'candidate_screening',
			python_callable = screen_candidates,
			op_kwargs = {
                        'base_dir': Variable.get("base_dir_var", default="./dags")
                        },
			dag=project_dag
			)

# task using hook to download interviewer data from S3
task3 = PythonOperator(
    task_id='s3_interviewer_data', # Keeping the same ID so the UI looks consistent
    python_callable=mock_interviewer_data,
    op_kwargs={
        'local_path': Variable.get('base_dir_var', default=fallback_dir)
    },
    dag=project_dag
)

# task to schedule interviews for the accepted candidates
task4 = PythonOperator(
			task_id = 'interview_scheduler',
			python_callable = schedule_candidates,
			op_kwargs = {
                        'base_dir': Variable.get('base_dir_var', default="./dags")
                        },
			dag = project_dag
			)

# task to give feedback to the interviewed candidates
task5 = PythonOperator(
			task_id = 'candidate_feedback',
			python_callable = feedback_status,
			op_kwargs = {
                        'base_dir': Variable.get('base_dir_var', default="./dags")
                        },
			dag = project_dag
			)
			
# task to onboard selected candidates
task6 = PythonOperator(
			task_id = 'candidate_onboarding',
			python_callable = onboard_candidates,
			op_kwargs = {
                'base_dir': Variable.get('base_dir_var', default="./dags")
                        },
			dag = project_dag
			)

# Task dependency
task1 >> task2 >> task3 >> task4 >> task5 >> task6
