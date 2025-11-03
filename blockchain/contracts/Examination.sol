// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

contract Examination {
    address public owner;
    uint public examIdCounter;

    struct Exam {
        uint id;
        string name;
        uint totalMarks;
        uint passingMarks;
        bool active;
    }

    mapping(uint => Exam) public exams;

    event ExamCreated(uint id, string name, uint totalMarks, uint passingMarks);
    event ExamUpdated(uint id, string name, uint totalMarks, uint passingMarks, bool active);

    constructor() {
        owner = msg.sender;
        examIdCounter = 0;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    function createExam(string memory _name, uint _totalMarks, uint _passingMarks) public onlyOwner {
        examIdCounter++;
        exams[examIdCounter] = Exam(examIdCounter, _name, _totalMarks, _passingMarks, true);
        emit ExamCreated(examIdCounter, _name, _totalMarks, _passingMarks);
    }

    function updateExam(uint _id, string memory _name, uint _totalMarks, uint _passingMarks, bool _active) public onlyOwner {
        require(exams[_id].id != 0, "Exam does not exist.");
        exams[_id] = Exam(_id, _name, _totalMarks, _passingMarks, _active);
        emit ExamUpdated(_id, _name, _totalMarks, _passingMarks, _active);
    }

    function getExam(uint _id) public view returns (uint, string memory, uint, uint, bool) {
        require(exams[_id].id != 0, "Exam does not exist.");
        Exam storage exam = exams[_id];
        return (exam.id, exam.name, exam.totalMarks, exam.passingMarks, exam.active);
    }
}