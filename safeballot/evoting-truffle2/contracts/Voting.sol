// SPDX-License-Identifier: MIT
/**  
File: Voting.sol
Purpose: This contract is designed to manage a basic voting process. It allows for the addition of candidates and casting votes. 
The contract maintains a list of candidates and ensures each address can vote only once. 
The contract also counts the votes for each candidate.` table.
Authors: Ella Brink, Lauren Wilson, Emma Bellai, Lucy DiSalvo 
Version History:
- Version 1.0 (Sprint 2): Initial version created by Ella Brink 
- Version 1.1 (Sprint 4): Updated voting logic by Lucy DiSalvo
*/

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
