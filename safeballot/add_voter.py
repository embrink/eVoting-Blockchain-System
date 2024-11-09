from database import add_voter
#manually load database
# Sample voter information
ssn = "333-33-333"
zipcode = "12345"
driver_id = "123-22-3456"

# Attempt to add the voter
voter_id = add_voter(ssn, zipcode, driver_id)

if voter_id:
    print(f"Voter added successfully with Voter ID: {voter_id}")
else:
    print("Failed to add voter. The SSN might already exist.")
