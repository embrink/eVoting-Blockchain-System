from voter import Voter
from admin import Admin
from auditor import Auditor
from config import load_contract

def main():
    role = input("Enter your role (voter, admin, auditor): ").strip().lower()
    contract = load_contract()
    
    if role == 'voter':
        ssn = input("Enter SSN: ")
        driver_id = input("Enter Driver ID: ")
        zipcode = input("Enter Zipcode: ")
        voter_account = "0xVoterAccountAddress"
        private_key = "VoterPrivateKey"
        voter = Voter(ssn, driver_id, zipcode, voter_account, private_key, contract)
        
        if voter.login():
            elections = voter.view_elections()
            print("Available elections:", elections)
            candidate_id = int(input("Enter candidate ID: "))
            voter.cast_vote(candidate_id)
        else:
            print("Invalid credentials.")

    elif role == 'admin':
        admin_id = input("Enter Admin ID: ")
        admin = Admin(admin_id, contract)
        
        if admin.login():
            action = input("Choose action (create_election/post_results): ").strip().lower()
            if action == "create_election":
                title = input("Enter title: ")
                start_time = int(input("Enter start time (epoch): "))
                end_time = int(input("Enter end time (epoch): "))
                admin.create_election(title, start_time, end_time)
            elif action == "post_results":
                candidate_id = int(input("Enter candidate ID: "))
                admin.post_results(candidate_id)
        else:
            print("Invalid credentials.")

    elif role == 'auditor':
        auditor_id = input("Enter Auditor ID: ")
        auditor = Auditor(auditor_id, contract)
        
        if auditor.login():
            action = input("Choose action (pull_statistics/approve_election): ").strip().lower()
            if action == "pull_statistics":
                candidate_id = int(input("Enter candidate ID: "))
                auditor.pull_voting_statistics(candidate_id)
            elif action == "approve_election":
                election_id = int(input("Enter election ID: "))
                auditor.approve_election(election_id)
        else:
            print("Invalid credentials.")

if __name__ == "__main__":
    main()
