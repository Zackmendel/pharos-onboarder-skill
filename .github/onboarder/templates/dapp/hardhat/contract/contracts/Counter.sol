// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract Counter {
    uint256 public number;

    function setNumber(uint256 newNumber) public {
        number = newNumber;
    }

    function increment() public {
        number++;
    }

    // Compatibility functions for Simple Storage integration
    function set(uint256 newNumber) public {
        number = newNumber;
    }

    // Get number
    function get() public view returns (uint256) {
        return number;
    }
}
