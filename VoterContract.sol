pragma solidity ^0.8.0;

contract Voting {
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    mapping(uint => Candidate) public candidates;
    mapping(address => bool) public voters;

    uint public candidateCount;

    constructor() {
        candidateCount = 0;
    }

    function addCandidate(string memory _name) public {
        candidateCount++;
        candidates[candidateCount] = Candidate(candidateCount, _name, 0);
    }

    function castVote(uint _candidateId) public {
        require(!voters[msg.sender], "You have already voted.");
        require(_candidateId > 0 && _candidateId <= candidateCount, "Invalid candidate.");

        voters[msg.sender] = true;
        candidates[_candidateId].voteCount++;
    }

    function getVoteCount(uint _candidateId) public view returns (uint) {
        return candidates[_candidateId].voteCount;
    }
}
