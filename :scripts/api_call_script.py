import pandas as pd
import random
import logging
# Removed numpy completely!

def api_call(base_dir):
    """
    Simulates a mock API extraction of candidate data.
    Initializes the 'God Payload' schema to establish a strict data contract
    for downstream tasks, utilizing pure Python null values to minimize 
    environment dependencies.
    """
    logging.info("Mocking API Call with the God Payload (No Numpy!)...")
    
    mock_data = {
        "candidate_id": random.randint(1000, 9999),
        "name": random.choice(["Alice Brown", "Bob Smith", "Charlie Davis", "Diana Prince"]),
        "gender": random.choice(["Female", "Male", "Male", "Female"]),
        "email": random.choice(["alice@example.com", "bob@example.com", "charlie@example.com", "diana@example.com"]),
        
        "applied_for": random.choice(["Engineering", "Sales", "Management", "HR", "Content"]),
        "applied_pos": random.choice(["SDE 1", "SDE 2", "HR Executive", "Content Editor"]),
        "years_of_experience": random.randint(0, 8),
        "skill_set": random.choice(["['Python', 'SQL']", "['Java', 'AWS']", "['Excel', 'Communication']", "['Salesforce']", "['Copywriting']"]),
        
        # Using Python's built-in 'None' instead of numpy
        "round_1_scheduled": None,
        "round_1_status": None,
        "round_2_scheduled": None,
        "round_2_status": None,
        
        "round_1_marks": None,
        "round_2_marks": None,
        "comments": None,
        "final_verdict": None,
        "overall_status": None,
        
        "offer_status": None,
        "joining_date": None,
        "offered_ctc": None,
        "background_check": None,
        
        # The extra trap we caught for Task 4
        "direct_offer_sent": None 
    }
    
    df = pd.DataFrame([mock_data])
    file_path = f"{base_dir}/candidate_resume.csv"
    df.to_csv(file_path, index=False)
    
    logging.info(f"Success! God Payload saved to {file_path}")
    return file_path
