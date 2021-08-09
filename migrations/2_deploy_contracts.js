var VaccinationPortal = artifacts.require("./VaccinationPortal.sol");

module.exports = function(deployer) {
  deployer.deploy(VaccinationPortal);
};
