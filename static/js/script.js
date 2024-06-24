// const attendanceForm = document.getElementById('attendance-form');
// const attendanceTable = document.getElementById('attendance-table');
// const messageElement = document.getElementById('message');

// // Function to add an attendance record to the table (replace with actual data retrieval logic)
// function addAttendanceRecord(name, timestamp) {
//   const tableBody = attendanceTable.getElementsByTagName('tbody')[0];
//   const tableRow = document.createElement('tr');
//   const nameCell = document.createElement('td');
//   const timestampCell = document.createElement('td');

//   nameCell.textContent = name;
//   timestampCell.textContent = timestamp;

//   tableRow.appendChild(nameCell);
//   tableRow.appendChild(timestampCell);
//   tableBody.appendChild(tableRow);
// }

// attendanceForm.addEventListener('submit', (event) => {
//   event.preventDefault(); // Prevent default form submission behavior

  
//   const name = document.getElementById('name').value.trim();

//   if (name) {
//     // Simulate successful attendance marking (replace with actual logic)
//     const timestamp = new Date().toLocaleString();
//     addAttendanceRecord(name, timestamp);
//     messageElement.textContent = `Attendance marked successfully for ${name}!`;
//     document.getElementById('name').value = ''; // Clear the name input field
//   } else {
//     messageElement.textContent = 'Please enter your name.';
//   }
// });


// Access form and feedback elements
const attendanceForm = document.getElementById('attendance-form');
const messageElement = document.getElementById('message');
const attendanceTable = document.getElementById('attendance-table');

// Function to handle form submission
attendanceForm.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent default form submission

  // Get student name from the form and trim whitespace
  const name = document.getElementById('name').value.trim();

  // Send student name to the backend for attendance marking
  fetch('/mark_attendance', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ names: name })
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      messageElement.textContent = data.error; // Display error message if any
    } else {
      // Display success message, timestamp, and name
      messageElement.textContent = `Attendance marked successfully for ${name} at ${data.timestamp}!`;

      // Add a new row to the attendance table with name and timestamp
      const tableBody = attendanceTable.getElementsByTagName('tbody')[0];
      const tableRow = document.createElement('tr');
      const nameCell = document.createElement('td');
      const timestampCell = document.createElement('td');

      nameCell.textContent = name;
      timestampCell.textContent = data.timestamp;

      tableRow.appendChild(nameCell);
      tableRow.appendChild(timestampCell);
      tableBody.appendChild(tableRow);

      // Clear the form
      attendanceForm.reset();
    }
  })
  .catch(error => {
    console.error('Error marking attendance:', error);
    messageElement.textContent = 'Failed to mark attendance. Please try again.';
  });
});
