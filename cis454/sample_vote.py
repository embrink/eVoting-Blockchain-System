nominee_1 = input("enter the nominee 1 name: ")
nominee_2 = input("enter the nominee 2 name: ")

n1_votes = 0
n2_votes = 0

voter_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

num_of_voters = len(voter_id)

while True:
    if voter_id ==[]:
        print("voting session over")
        if n1_votes > n2_votes:
            p = (n1_votes/num_of_voters)*100
            print(nominee_1, "has won with ", p, "% votes ")
            
        elif n2_votes > n1_votes:
            p = (n2_votes/num_of_voters)*100
            print(nominee_2, "has won with ", p, "% votes ")
        break
    else:    
        voter = int(input("enter your voter id number: "))
        if voter in voter_id:
            print("you are a voter ")
            voter_id.remove(voter)
            vote = input(f"enter your vote for {nominee_1} or {nominee_2}: ")
            if vote == nominee_1:
                n1_votes += 1
                print("thank you for casting your vote")
            elif vote == nominee_2:
                n2_votes+=1

        else:
            print("vote already casted or voting ineligible")