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