// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

contract Examination {
    address public owner;
    uint public examIdCounter;

    enum Role { None, Teacher, Student }
    mapping(address => Role) public userRoles;

    struct Exam {
        uint id;
        string name;
        uint totalMarks;
        uint passingMarks;
        bool active;
    }

    mapping(uint => Exam) public exams;

    struct Submission {
        uint examId;
        address studentAddress;
        string answersHash; // Hash of the student's answers
        uint grade; // 0 if not graded, otherwise the score
        bool graded;
    }

    mapping(uint => mapping(address => Submission)) public submissions;

    event ExamCreated(uint id, string name, uint totalMarks, uint passingMarks);
    event ExamUpdated(uint id, string name, uint totalMarks, uint passingMarks, bool active);
    event RoleAssigned(address indexed user, Role newRole);
    event ExamSubmitted(uint examId, address indexed studentAddress, string answersHash);
    event ExamGraded(uint examId, address indexed studentAddress, uint grade);

    constructor() {
        owner = msg.sender;
        examIdCounter = 0;
        userRoles[owner] = Role.Teacher; // Owner is also a teacher by default
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    modifier onlyTeacher() {
        require(userRoles[msg.sender] == Role.Teacher, "Only teachers can call this function.");
        _;
    }

    modifier onlyStudent() {
        require(userRoles[msg.sender] == Role.Student, "Only students can call this function.");
        _;
    }

    function assignRole(address _user, Role _role) public onlyOwner {
        require(_user != address(0), "Invalid address.");
        userRoles[_user] = _role;
        emit RoleAssigned(_user, _role);
    }

    function getRole(address _user) public view returns (Role) {
        return userRoles[_user];
    }

    function createExam(string memory _name, uint _totalMarks, uint _passingMarks) public onlyTeacher {
        examIdCounter++;
        exams[examIdCounter] = Exam(examIdCounter, _name, _totalMarks, _passingMarks, true);
        emit ExamCreated(examIdCounter, _name, _totalMarks, _passingMarks);
    }

    function updateExam(uint _id, string memory _name, uint _totalMarks, uint _passingMarks, bool _active) public onlyTeacher {
        require(exams[_id].id != 0, "Exam does not exist.");
        exams[_id] = Exam(_id, _name, _totalMarks, _passingMarks, _active);
        emit ExamUpdated(_id, _name, _totalMarks, _passingMarks, _active);
    }

    function getExam(uint _id) public view returns (uint, string memory, uint, uint, bool) {
        require(exams[_id].id != 0, "Exam does not exist.");
        Exam storage exam = exams[_id];
        return (exam.id, exam.name, exam.totalMarks, exam.passingMarks, exam.active);
    }

    function submitExam(uint _examId, string memory _answersHash) public onlyStudent {
        require(exams[_examId].id != 0, "Exam does not exist.");
        require(exams[_examId].active, "Exam is not active for submissions.");
        require(submissions[_examId][msg.sender].examId == 0, "Exam already submitted by this student.");

        submissions[_examId][msg.sender] = Submission(_examId, msg.sender, _answersHash, 0, false);
        emit ExamSubmitted(_examId, msg.sender, _answersHash);
    }

    function gradeExam(uint _examId, address _studentAddress, uint _grade) public onlyTeacher {
        require(exams[_examId].id != 0, "Grade Exam: Exam does not exist.");
        require(submissions[_examId][_studentAddress].examId != 0, "Grade Exam: Submission not found for this student.");
        require(!submissions[_examId][_studentAddress].graded, "Grade Exam: Exam already graded.");
        require(_grade <= exams[_examId].totalMarks, "Grade Exam: Grade exceeds total marks.");

        submissions[_examId][_studentAddress].grade = _grade;
        submissions[_examId][_studentAddress].graded = true;
        emit ExamGraded(_examId, _studentAddress, _grade);
    }

    function getSubmission(uint _examId, address _studentAddress) public view returns (uint, address, string memory, uint, bool) {
        require(submissions[_examId][_studentAddress].examId != 0, "Submission not found.");
        Submission storage submission = submissions[_examId][_studentAddress];
        return (submission.examId, submission.studentAddress, submission.answersHash, submission.grade, submission.graded);
    }

    function getExamIdCounter() public view returns (uint) {
        return examIdCounter;
    }
}