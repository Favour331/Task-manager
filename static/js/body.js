// function add_item(){
//     document.getElementById('mainer').style.display = 'grid';
//     document.getElementById('mains').style.display = 'none';
// }

// Add event listeners to checkboxes for crossing out p tags and update status in DB
document.addEventListener('DOMContentLoaded', function() {
    // Attach to all checkboxes (table rows and card views)
    const checkboxes = document.querySelectorAll('.cross-toggle');
    checkboxes.forEach(function(checkbox) {
        // determine the container (tr or .card)
        const rowContainer = checkbox.closest('tr');
        const cardContainer = checkbox.closest('.card');
        const container = rowContainer || cardContainer;

        // helper to find status text and crossable elements within the same container
        const statusTextElems = container ? container.querySelectorAll('.status-text') : [];
        const crossableElems = container ? container.querySelectorAll('.crossable') : [];
        const editBtn = container ? container.querySelector('a[href^="/edit_task/"]') : null;

        // set initial edit button state and initial crossed state
        if (editBtn && checkbox.checked) {
            editBtn.setAttribute('disabled', 'disabled');
            editBtn.style.pointerEvents = 'none';
            editBtn.style.opacity = '0.5';
            editBtn.style.background = 'gray';
        }
        if (checkbox.checked) {
            // apply line-through to crossable elements initially
            crossableElems.forEach(function(el) {
                el.style.textDecoration = 'line-through';
            });
        }

        checkbox.addEventListener('change', function() {
            const taskId = checkbox.getAttribute('data-task-id');
            const status = checkbox.checked ? 'Completed' : 'Pending';

            fetch(`/update_status/${taskId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `status=${encodeURIComponent(status)}`
            }).then(response => {
                if (!response.ok) throw new Error('Network response was not ok');

                // update UI only after server confirms
                // update status text elements (no line-through)
                statusTextElems.forEach(function(el) {
                    el.textContent = status;
                });

                // apply line-through to crossable elements
                crossableElems.forEach(function(el) {
                    if (status === 'Completed') el.style.textDecoration = 'line-through';
                    else el.style.textDecoration = 'none';
                });

                // toggle edit button
                if (editBtn) {
                    if (status === 'Completed') {
                        editBtn.setAttribute('disabled', 'disabled');
                        editBtn.style.pointerEvents = 'none';
                        editBtn.style.opacity = '0.5';
                        editBtn.style.background = 'gray';
                    } else {
                        editBtn.removeAttribute('disabled');
                        editBtn.style.pointerEvents = '';
                        editBtn.style.opacity = '';
                        editBtn.style.background = 'rgb(63, 63, 19)';
                    }
                }
            }).catch(err => {
                console.error('Failed to update status:', err);
                // revert checkbox if update failed
                checkbox.checked = !checkbox.checked;
            });
        });
    });
});