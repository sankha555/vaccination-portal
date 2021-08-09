// SPDX-License-Identifier: MIT
pragma solidity 0.5.16;

contract VaccinationPortal {
    struct Citizen {
        string pseudoUUID;
        string secretCode;
        string staticKey;
        uint doses;
    }

    struct Center {
        address account;
        string centerID;
        string centerAddress;
        string staticKey;
        int16 numVaccinations;
    }

    struct Vaccination {
        string vaccinationID;
        string citizenPseudoUUID;
        string vaccineName;
        uint doseNumber;
        string centerID;
        string healthInfo;
    }

    /* STATE VARIABLES */
    address public govtAgency; // the government agency overseeing this chain
    
    mapping(string => Citizen) public citizens;
    mapping(string => Center) public centers; 
    mapping(string => Vaccination) public vaccinations;
    
    uint public totalCitizens;    
    uint public totalCenters;    
    uint public totalVaccinations;    
    
    /* Constructor and methods */
    constructor () public {
        govtAgency = msg.sender;
        totalCitizens = 0;
        totalCenters = 0;
        totalVaccinations = 0;
    }

    function registerCitizen(
        string memory _pseudoUUID, 
        string memory _secretCode, 
        string memory _staticKey
    ) public {
        require(msg.sender == govtAgency);

        citizens[_pseudoUUID] = Citizen(_pseudoUUID, _secretCode, _staticKey, 0);
        totalCitizens++;
    }

    function registerCenter(
        string memory _centerID,
        string memory _centerAddress,
        string memory _staticKey
    ) public {
        centers[_centerID] = Center(msg.sender, _centerID, _centerAddress, _staticKey, 0);
        totalCenters++;
    }

    function vaccinate(
        string memory _vaccinationID,
        string memory _citizenPseudoUUID,
        string memory _vaccineName,
        uint _doseNumber,
        string memory _centerID,
        string memory _healthInfo
    ) public {
        Citizen memory citizen = citizens[_citizenPseudoUUID];
        require(citizen.doses < 2 && citizen.doses < _doseNumber);
        
        Center memory center = centers[_centerID];
        require(center.account == msg.sender);

        vaccinations[_vaccinationID] = Vaccination(
            _vaccinationID, _citizenPseudoUUID, _vaccineName, _doseNumber, _centerID, _healthInfo
        );

        citizen.doses++;
        center.numVaccinations++;

        totalVaccinations++;
    }
}
