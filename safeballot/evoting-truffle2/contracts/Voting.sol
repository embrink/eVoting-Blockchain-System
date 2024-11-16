// SPDX-License-Identifier: MIT
// File: Voting.sol
// Purpose: This contract implements a simple voting system on the Ethereum blockchain. 
// It allows users to vote for candidates, ensures that each address can only vote once, 
// and provides functionality to add new candidates.
// Authors: Lucy DiSalvo, Lauren Wilson, Emma Bellai, Ella Brink
// Version History:
// - Version 1.0 (Sprint 3): Initial version with functionality to add candidates and cast votes.
// - Version 1.1 (Sprint 4): Updated constructor to initialize with two candidates ("Alice" and "Bob") by Lucy DiSalvo
// - Version 1.3 (Sprint 4): Added public visibility for candidate and voter mappings for easy data retrieval by Lucy DiSalvo
// - Version 1.4 (Sprint 4): Documentation added for clarity and maintainability by Lucy DiSalvo

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
