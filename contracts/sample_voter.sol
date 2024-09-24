// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Voting {
    // Structure for a single voter
    struct Voter {
        bool voted;       // If true, the voter has already voted
        uint256 vote;     // Index of the voted proposal
        bool authorized;  // If true, the voter is authorized to vote
    }

    // Structure for a single proposal
    struct Proposal {
        string name;      // Name of the proposal
        uint256 voteCount; // Number of votes the proposal has received
    }

    // Owner of the contract (usually the one who deploys it)
    address public owner;

    // List of voters (mapped by their addresses)
    mapping(address => Voter) public voters;

    // List of proposals
    Proposal[] public proposals;

    // Constructor to initialize the contract with a list of proposal names
    constructor(string[] memory proposalNames) {
        // Set the owner of the contract
        owner = msg.sender;

        // Add each proposal name to the list of proposals
        for (uint256 i = 0; i < proposalNames.length; i++) {
            proposals.push(Proposal({
                name: proposalNames[i],
                voteCount: 0
            }));
        }
    }

    // Modifier to restrict function access to only the owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the contract owner can call this function.");
        _;
    }

    // Function to authorize a voter (only owner can authorize)
    function authorizeVoter(address voter) public onlyOwner {
        voters[voter].authorized = true;
    }

    // Function to vote for a proposal
    function vote(uint256 proposalIndex) public {
        // Check if the voter is authorized and has not voted yet
        require(voters[msg.sender].authorized, "You are not authorized to vote.");
        require(!voters[msg.sender].voted, "You have already voted.");

        // Record the vote
        voters[msg.sender].voted = true;
        voters[msg.sender].vote = proposalIndex;

        // Increment the vote count for the selected proposal
        proposals[proposalIndex].voteCount++;
    }

    // Function to get the winning proposal
    function winningProposal() public view returns (uint256 winningProposalIndex) {
        uint256 winningVoteCount = 0;

        // Loop through all proposals to find the one with the most votes
        for (uint256 i = 0; i < proposals.length; i++) {
            if (proposals[i].voteCount > winningVoteCount) {
                winningVoteCount = proposals[i].voteCount;
                winningProposalIndex = i;
            }
        }
    }

    // Function to get the name of the winning proposal
    function winnerName() public view returns (string memory winner) {
        // Get the index of the winning proposal
        winner = proposals[winningProposal()].name;
    }
}
