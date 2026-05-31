import pandas as pd
import random

def onboard_candidates(base_dir):
    
    """
    Reads screened candidate metadata, filters for passed rounds or direct offers,
    and generates randomized onboarding payroll data (Employee ID, Aadhar, PAN).
    Appends the final records to the existing onboarded candidates staging file.
    """

    meta_data_df = pd.read_csv(base_dir + '/interview_metadata.csv')
    
    onboard_df = pd.read_csv(base_dir + '/onboarded_candidates.csv')

    def filter_candidates(meta_data_df):
        condition = (meta_data_df['round_2_status'] == 'Pass') | (meta_data_df['direct_offer_sent'] == 'Yes')
        df = meta_data_df.loc[condition, :]
        return df

    def random_personal_data():
        emp_number = ''.join([str(random.choice(range(0, 9))) for i in range(0, 5)])
        aadhar_number = ''.join([str(random.choice(range(0, 10))) for i in range(0, 11)])
        pan_number = ''.join([''.join([chr(random.choice(range(97, 123))), str(random.choice(range(0, 10)))]) for i in range(0, 6)])
        return emp_number, aadhar_number, pan_number

    filtered_df = filter_candidates(meta_data_df)
    filtered_df.reset_index(inplace=True, drop=True)

    # Convert to set safely
    existing_emails = set(onboard_df['email'].values) if 'email' in onboard_df.columns else set()
    
    # 2. FIXED: Proper indentation for the loop!
    for i in range(len(filtered_df)):
        # 3. FIXED: Changed 'candidate_email' to 'email' to prevent KeyError
        if filtered_df.loc[i, 'email'] in existing_emails:
            filtered_df.drop(i, axis=0, inplace=True)

    if filtered_df.shape[0] == 0:
        pass
    else:
        sample_size = random.randint(1, filtered_df.shape[0])
        random_indexes = random.sample(range(0, filtered_df.shape[0]), sample_size)
        
        for filter_indx in random_indexes:
            onboard_indx = onboard_df.shape[0]
            emp_number, aadhar_number, pan_number = random_personal_data()
            
            onboard_df.loc[onboard_indx, 'employee_id'] = emp_number
            # 3. FIXED: Changed 'candidate_name' to 'name' to prevent KeyError
            onboard_df.loc[onboard_indx, 'name'] = filtered_df.loc[filter_indx, 'name']
            onboard_df.loc[onboard_indx, 'gender'] = filtered_df.loc[filter_indx, 'gender']
            onboard_df.loc[onboard_indx, 'email'] = filtered_df.loc[filter_indx, 'email']
            onboard_df.loc[onboard_indx, 'aadhar'] = aadhar_number
            onboard_df.loc[onboard_indx, 'pan'] = pan_number

    # save onboarded candidates file
    onboard_df.to_csv(base_dir + '/onboarded_candidates.csv', index=False)
