// File: 2_deploy_voting.js
// Purpose: This migration script deploys the Voting smart contract to the blockchain.
// It automates the deployment process using Truffle's migration framework.
// Authors: Lucy DiSalvo, Lauren Wilson, Emma Bellai, Ella Brink
// Version History:
// - Version 1.0 (Sprint 3): Initial version deploying the Voting contract by Lucy DiSalvo
// - Version 1.1 (Sprint 4): Added logging for deployment status and contract address by Lucy DiSalvo
// - Version 1.2 (Sprint 4): (Commented out) Deployment logic for VoterContract by Lucy DiSalvo for future implementation.



const Voting = artifacts.require("Voting");
//const VoterContract = artifacts.require("VoterContract");

module.exports = async function(deployer) {
  console.log("Deploying Voting contract...");
  await deployer.deploy(Voting);
  const votingInstance = await Voting.deployed();
  console.log("Voting contract deployed at:", votingInstance.address);

 // console.log("Deploying VoterContract with Voting address...");
 // await deployer.deploy(VoterContract, votingInstance.address);
  //console.log("VoterContract deployed.");
};
