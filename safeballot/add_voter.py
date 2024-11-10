# Function: add_voter
# Purpose: Adds a new voter to the database using their SSN, zipcode, and driver ID. 
# The function generates a unique voter ID and attempts to insert the new voter into the `voters` table.
# Authors: Ella Brink, Lauren Wilson, Emma Bellai, Lucy DiSalvo 
# Version History:
# - Version 1.0 (Sprint 2): Initial version created by Ella Brink 
# - Version 1.1 (Sprint 4): Added documentation by Lucy DiSalvo 

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
