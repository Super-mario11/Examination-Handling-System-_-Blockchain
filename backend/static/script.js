let loggedInAddress = null;
let loggedInRole = null;

function showDashboard(role) {
    document.getElementById('teacherDashboard').style.display = 'none';
    document.getElementById('studentDashboard').style.display = 'none';
    document.getElementById('publicView').style.display = 'block'; // Always show public view

    if (role === 'Teacher') {
        document.getElementById('teacherDashboard').style.display = 'block';
    } else if (role === 'Student') {
        document.getElementById('studentDashboard').style.display = 'block';
    }
}

document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const statusElement = document.getElementById('loginStatus');
    const loggedInUserRoleElement = document.getElementById('loggedInUserRole');
    statusElement.innerText = 'Logging in...';
    loggedInUserRoleElement.innerText = '';

    const loginAddress = document.getElementById('loginAddress').value;

    try {
        const response = await fetch(`/get-role/${loginAddress}`);
        const data = await response.json();
        if (response.ok) {
            loggedInAddress = loginAddress;
            loggedInRole = data.role;
            loggedInUserRoleElement.innerText = `Logged in as: ${loggedInAddress} (Role: ${loggedInRole})`;
            statusElement.innerText = 'Login successful.';
            showDashboard(loggedInRole);
        } else {
            statusElement.innerText = `Error: ${data.error}`;
            loggedInAddress = null;
            loggedInRole = null;
            showDashboard(null); // Show only public view
        }
    } catch (error) {
        console.error('Error during login:', error);
        statusElement.innerText = 'Error during login.';
        loggedInAddress = null;
        loggedInRole = null;
        showDashboard(null); // Show only public view
    }
});

// Initial display
showDashboard(null);

document.getElementById('deployContract').addEventListener('click', async () => {
    const statusElement = document.getElementById('deploymentStatus');
    statusElement.innerText = 'Deploying contract...';

    try {
        const response = await fetch('/deploy-contract', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const data = await response.json();
        if (response.ok) {
            statusElement.innerText = data.message;
        } else {
            statusElement.innerText = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error deploying contract:', error);
        statusElement.innerText = 'Error deploying contract.';
    }
});

document.getElementById('assignRoleForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const statusElement = document.getElementById('assignRoleStatus');
    statusElement.innerText = 'Assigning role...';

    const userAddress = document.getElementById('userAddress').value;
    const role = document.getElementById('role').value;

    try {
        const response = await fetch('/assign-role', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userAddress: userAddress, role: role }),
        });
        const data = await response.json();
        if (response.ok) {
            statusElement.innerText = data.message;
        } else {
            statusElement.innerText = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error assigning role:', error);
        statusElement.innerText = 'Error assigning role.';
    }
});

document.getElementById('getRoleForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const statusElement = document.getElementById('getRoleStatus');
    const userRoleElement = document.getElementById('userRole');
    statusElement.innerText = 'Fetching role...';
    userRoleElement.innerText = '';

    const getRoleAddress = document.getElementById('getRoleAddress').value;

    try {
        const response = await fetch(`/get-role/${getRoleAddress}`);
        const data = await response.json();
        if (response.ok) {
            userRoleElement.innerText = `Role: ${data.role}`;
            statusElement.innerText = 'Role fetched successfully.';
        } else {
            statusElement.innerText = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error fetching role:', error);
        statusElement.innerText = 'Error fetching role.';
    }
});

document.getElementById('createExamForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const statusElement = document.getElementById('createExamStatus');
    statusElement.innerText = 'Creating exam...';

    const examName = document.getElementById('examName').value;
    const totalMarks = document.getElementById('totalMarks').value;
    const passingMarks = document.getElementById('passingMarks').value;

    try {
        const response = await fetch('/create-exam', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: examName, totalMarks: totalMarks, passingMarks: passingMarks }),
        });
        const data = await response.json();
        if (response.ok) {
            statusElement.innerText = data.message;
        } else {
            statusElement.innerText = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error creating exam:', error);
        statusElement.innerText = 'Error creating exam.';
    }
});

document.getElementById('getExamForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const statusElement = document.getElementById('getExamStatus');
    const examDetailsDiv = document.getElementById('examDetails');
    statusElement.innerText = 'Fetching exam...';
    examDetailsDiv.innerHTML = '';

    const examId = document.getElementById('getExamId').value;

    try {
        const response = await fetch(`/get-exam/${examId}`);
        const data = await response.json();
        if (response.ok) {
            examDetailsDiv.innerHTML = `
                <p><strong>ID:</strong> ${data.id}</p>
                <p><strong>Name:</strong> ${data.name}</p>
                <p><strong>Total Marks:</strong> ${data.totalMarks}</p>
                <p><strong>Passing Marks:</strong> ${data.passingMarks}</p>
                <p><strong>Active:</strong> ${data.active}</p>
            `;
            statusElement.innerText = 'Exam fetched successfully.';
        } else {
            examDetailsDiv.innerHTML = '';
            statusElement.innerText = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error fetching exam:', error);
        statusElement.innerText = 'Error fetching exam.';
    }
});

document.getElementById('updateExamForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const statusElement = document.getElementById('updateExamStatus');
    statusElement.innerText = 'Updating exam...';

    const examId = document.getElementById('updateExamId').value;
    const examName = document.getElementById('updateExamName').value;
    const totalMarks = document.getElementById('updateTotalMarks').value;
    const passingMarks = document.getElementById('updatePassingMarks').value;
    const active = document.getElementById('updateActive').checked;

    try {
        const response = await fetch('/update-exam', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: examId, name: examName, totalMarks: totalMarks, passingMarks: passingMarks, active: active }),
        });
        const data = await response.json();
        if (response.ok) {
            statusElement.innerText = data.message;
        } else {
            statusElement.innerText = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error updating exam:', error);
        statusElement.innerText = 'Error updating exam.';
    }
});

document.getElementById('submitExamForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const statusElement = document.getElementById('submitExamStatus');
    statusElement.innerText = 'Submitting exam...';

    const examId = document.getElementById('submitExamId').value;
    const answersHash = document.getElementById('answersHash').value;

    try {
        const response = await fetch('/submit-exam', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ examId: examId, answersHash: answersHash, studentAddress: loggedInAddress }),
        });
        const data = await response.json();
        if (response.ok) {
            statusElement.innerText = data.message;
        } else {
            statusElement.innerText = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error submitting exam:', error);
        statusElement.innerText = 'Error submitting exam.';
    }
});

document.getElementById('gradeExamForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const statusElement = document.getElementById('gradeExamStatus');
    statusElement.innerText = 'Grading exam...';

    const examId = document.getElementById('gradeExamId').value;
    const studentAddress = document.getElementById('studentAddress').value;
    const grade = document.getElementById('grade').value;

    try {
        const response = await fetch('/grade-exam', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ examId: examId, studentAddress: studentAddress, grade: grade }),
        });
        const data = await response.json();
        if (response.ok) {
            statusElement.innerText = data.message;
        } else {
            statusElement.innerText = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error grading exam:', error);
        statusElement.innerText = 'Error grading exam.';
    }
});

document.getElementById('getSubmissionForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const statusElement = document.getElementById('getSubmissionStatus');
    const submissionDetailsDiv = document.getElementById('submissionDetails');
    statusElement.innerText = 'Fetching submission...';
    submissionDetailsDiv.innerHTML = '';

    const examId = document.getElementById('getSubmissionExamId').value;
    const studentAddress = document.getElementById('getSubmissionStudentAddress').value;

    try {
        const response = await fetch(`/get-submission/${examId}/${studentAddress}`);
        const data = await response.json();
        if (response.ok) {
            submissionDetailsDiv.innerHTML = `
                <p><strong>Exam ID:</strong> ${data.examId}</p>
                <p><strong>Student Address:</strong> ${data.studentAddress}</p>
                <p><strong>Answers Hash:</strong> ${data.answersHash}</p>
                <p><strong>Grade:</strong> ${data.grade}</p>
                <p><strong>Graded:</strong> ${data.graded}</p>
            `;
            statusElement.innerText = 'Submission fetched successfully.';
        } else {
            submissionDetailsDiv.innerHTML = '';
            statusElement.innerText = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error fetching submission:', error);
        statusElement.innerText = 'Error fetching submission.';
    }
});

document.getElementById('getAllExams').addEventListener('click', async () => {
    const statusElement = document.getElementById('getAllExamsStatus');
    const allExamsListDiv = document.getElementById('allExamsList');
    statusElement.innerText = 'Fetching all exams...';
    allExamsListDiv.innerHTML = '';

    try {
        const counterResponse = await fetch('/get-exam-id-counter');
        const counterData = await counterResponse.json();
        if (!counterResponse.ok) {
            statusElement.innerText = `Error: ${counterData.error}`;
            return;
        }
        const examIdCounter = counterData.examIdCounter;

        if (examIdCounter === 0) {
            statusElement.innerText = 'No exams created yet.';
            return;
        }

        let examsHtml = '<h3>Available Exams:</h3><ul>';
        for (let i = 1; i <= examIdCounter; i++) {
            const examResponse = await fetch(`/get-exam/${i}`);
            const examData = await examResponse.json();
            if (examResponse.ok) {
                examsHtml += `
                    <li>
                        <strong>ID:</strong> ${examData.id}<br>
                        <strong>Name:</strong> ${examData.name}<br>
                        <strong>Total Marks:</strong> ${examData.totalMarks}<br>
                        <strong>Passing Marks:</strong> ${examData.passingMarks}<br>
                        <strong>Active:</strong> ${examData.active}
                    </li>
                `;
            } else {
                examsHtml += `<li>Error fetching exam ${i}: ${examData.error}</li>`;
            }
        }
        examsHtml += '</ul>';
        allExamsListDiv.innerHTML = examsHtml;
        statusElement.innerText = 'All exams fetched successfully.';
    } catch (error) {
        console.error('Error fetching all exams:', error);
        statusElement.innerText = 'Error fetching all exams.';
    }
});