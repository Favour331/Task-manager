// function add_item(){
//     document.getElementById('mainer').style.display = 'grid';
//     document.getElementById('mains').style.display = 'none';
// }

// Add event listeners to checkboxes for crossing out p tags and update status in DB
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card) {
        const checkbox = card.querySelector('.cross-toggle');
        const ps = card.querySelectorAll('.crossable');
        if (checkbox) {
            // Disable edit button if already completed
            if (checkbox.checked) {
                const editBtn = card.querySelector('a[href^="/edit_task/"]');
                if (editBtn) {
                    editBtn.setAttribute('disabled', 'disabled');
                    editBtn.style.pointerEvents = 'none';
                    editBtn.style.opacity = '0.5';
                    editBtn.style.background = 'gray';
                }
            }
            checkbox.addEventListener('change', function() {
                ps.forEach(function(p) {
                    if (checkbox.checked) {
                        p.style.textDecoration = 'line-through';
                    } else {
                        p.style.textDecoration = 'none';
                    }
                });
                // Send status update to server
                const taskId = checkbox.getAttribute('data-task-id');
                const status = checkbox.checked ? 'Completed' : 'Pending';
                fetch(`/update_status/${taskId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `status=${encodeURIComponent(status)}`
                });
                // Disable edit button if checked
                const editBtn = card.querySelector('a[href^="/edit_task/"]');
                if (editBtn) {
                    if (checkbox.checked) {
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
            });
        }
    });
});