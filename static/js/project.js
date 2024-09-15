document.getElementById('addTaskButton').onclick = function() {
    document.getElementById('addTaskModal').style.display = 'block';
}

document.querySelector('.close').onclick = function() {
    document.getElementById('addTaskModal').style.display = 'none';
}

// Close the modal if user clicks outside the modal content
window.onclick = function(event) {
    if (event.target == document.getElementById('addTaskModal')) {
        document.getElementById('addTaskModal').style.display = 'none';
    }
}

// Submit the form via AJAX
document.getElementById('taskForm').onsubmit = function(event) {
    event.preventDefault(); // Prevent default form submission
    
    let formData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        deadline: document.getElementById('deadline').value,
        project_id: document.getElementById('project_id').value,
        priority: document.getElementById('priority').value
    };

    fetch('/add_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Add the new task to the task list dynamically
            let taskList = document.getElementById('taskList'); // Assuming taskList is an existing element on the project page
            let newTask = document.createElement('li');
            newTask.textContent = `${data.task.title} - ${data.task.description}`;
            taskList.appendChild(newTask);

            // Close the modal
            document.getElementById('addTaskModal').style.display = 'none';

            // Optionally clear the form
            document.getElementById('taskForm').reset();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}