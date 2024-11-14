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
