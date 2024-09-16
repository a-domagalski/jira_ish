document.getElementById('addTaskButton').onclick = function() {
    document.getElementById('addTaskModal').style.display = 'block';
}

document.querySelector('.close').onclick = function() {
    document.getElementById('addTaskModal').style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == document.getElementById('addTaskModal')) {
        document.getElementById('addTaskModal').style.display = 'none';
    }
}

document.getElementById('taskForm').onsubmit = function(event) {
    event.preventDefault();
    
    let formData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        deadline: document.getElementById('deadline').value,
        project_id: document.getElementById('project_id').value,
        priority: document.getElementById('priority').value,
        status: 'backlog'
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
            let tasksList = document.querySelector('#backlog .tasksList');
            let newTask = document.createElement('li');
            newTask.classList.add('task');
            newTask.setAttribute('id', `${data.task.id}`);
            newTask.textContent = `${data.task.title} - ${data.task.description}`;

            tasksList.appendChild(newTask);

            $(newTask).draggable({
                revert: "invalid",
                // stack: ".task",
                cursor: "move",
                containment: "body"
            });
            resizeContainerIfNeeded();

            $(".taskState").droppable({
                accept: ".task",
                drop: function(event, ui) {
                    let droppedTask = ui.helper.clone();
                    let originalTask = ui.draggable;
        
                    $(this).find('.tasksList').append(droppedTask);
                    let sectoinStatus = $(this).attr('id');
                    
                    originalTask.remove();
                    //TODO delete method request
                    
                    droppedTask.draggable({
                        revert: "invalid",
                        cursor: "move",
                        containment: "body",
                        helper: "clone",
                        start: function(event, ui) {
                            $(this).css('opacity', '0.5');
                        },
                        stop: function(event, ui) {
                            $(this).css('opacity', '1');
                        }
                    });
                    let updateData = {
                        status: sectoinStatus
                    };
                    let droppedTaskId = droppedTask.attr('id');
                    fetch(`/update_task/${droppedTaskId}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(updateData),
                    });
                    // .then(response => response.json())
                    // .then(data => {
                        
                    // })
                }

            });
            document.getElementById('addTaskModal').style.display = 'none';

            document.getElementById('taskForm').reset();
        } else {
            console.error('Error: Task creation failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function resizeContainerIfNeeded() {
    let maxHeight = 0;
    $('.sectionsGrid').each(function() {
        let currentHeight = $(this).outerHeight();
        if (currentHeight > maxHeight) {
            maxHeight = currentHeight;
        }
    });
    $('.container').css('height', maxHeight + 'px');
}