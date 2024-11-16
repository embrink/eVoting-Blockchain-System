// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    struct Candidate {
        uint256 id;
        string name;
        uint256 voteCount;
    }

    mapping(uint256 => Candidate) public candidates;
    mapping(address => bool) public voters;
    uint256 public candidatesCount;

    constructor() {
        addCandidate("Alice");
        addCandidate("Bob");
    }

    function addCandidate(string memory name) public {
        candidatesCount++;
        candidates[candidatesCount] = Candidate(candidatesCount, name, 0);
    }

    function vote(uint256 candidateId) public {
        require(!voters[msg.sender], "You have already voted.");
        require(candidateId > 0 && candidateId <= candidatesCount, "Invalid candidate.");

        voters[msg.sender] = true;
        candidates[candidateId].voteCount++;
    }
}
