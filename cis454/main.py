from user import register_user, login
from election import create_election, get_active_elections
from voting import cast_vote
from audit import view_election_statistics

def main():
    while True:
        print("\n1. Register User\n2. Login\n3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role (voter/admin/auditor): ")
            try:
                register_user(username, password, role)
                print("User registered successfully.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_info = login(username, password)
            
            if user_info:
                user_id, role = user_info
                print(f"Logged in as {role}.")
                
                # Provide role-based menu
                while True:
                    if role == 'voter':
                        print("\n1. View Active Elections\n2. Cast Vote\n3. Logout")
                        voter_choice = input("Choose an option: ")

                        if voter_choice == '1':
                            elections = get_active_elections()
                            if elections:
                                print("Active Elections:")
                                for election in elections:
                                    print(f"ID: {election[0]}, Name: {election[1]}")
                            else:
                                print("No active elections available.")
                        elif voter_choice == '2':
                            election_id = input("Enter election ID to vote in: ")
                            candidate_id = input("Enter candidate ID to vote for: ")
                            try:
                                cast_vote(user_id, election_id, candidate_id)
                                print("Vote cast successfully.")
                            except Exception as e:
                                print(f"Error: {e}")
                        elif voter_choice == '3':
                            break
                        else:
                            print("Invalid option.")
                    
                    elif role == 'admin':
                        print("\n1. Create Election\n2. Post Results\n3. Logout")
                        admin_choice = input("Choose an option: ")

                        if admin_choice == '1':
                            name = input("Enter election name: ")
                            start_date = input("Enter start date (YYYY-MM-DD): ")
                            end_date = input("Enter end date (YYYY-MM-DD): ")
                            try:
                                create_election(name, start_date, end_date)
                                print("Election created successfully.")
                            except Exception as e:
                                print(f"Error: {e}")
                        elif admin_choice == '2':
                            # Functionality for posting results can be added here
                            print("Post Results feature not implemented yet.")
                        elif admin_choice == '3':
                            break
                        else:
                            print("Invalid option.")
                    
                    elif role == 'auditor':
                        print("\n1. View Election Statistics\n2. Logout")
                        auditor_choice = input("Choose an option: ")

                        if auditor_choice == '1':
                            election_id = input("Enter election ID: ")
                            try:
                                statistics = view_election_statistics(election_id)
                                print("Election Statistics:")
                                print(statistics)
                            except Exception as e:
                                print(f"Error: {e}")
                        elif auditor_choice == '2':
                            break
                        else:
                            print("Invalid option.")
            else:
                print("Invalid credentials.")

        elif choice == '3':
            print("Exiting system.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
