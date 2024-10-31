// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    address public admin;
    mapping(address => bool) public eligibleVoters;
    mapping(address => bool) public hasVoted;
    mapping(uint => uint) public votes; // candidateID => vote count

    event VoteCast(address indexed voter, uint candidateId);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only the admin can perform this action");
        _;
    }

    modifier onlyEligibleVoter() {
        require(eligibleVoters[msg.sender], "You are not eligible to vote");
        require(!hasVoted[msg.sender], "You have already voted");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    function assignVoter(address _voter) public onlyAdmin {
        eligibleVoters[_voter] = true;
    }

    function castVote(uint _candidateId) public onlyEligibleVoter {
        votes[_candidateId]++;
        hasVoted[msg.sender] = true;
        emit VoteCast(msg.sender, _candidateId);
    }

    function getVoteCount(uint _candidateId) public view returns (uint) {
        return votes[_candidateId];
    }
}
