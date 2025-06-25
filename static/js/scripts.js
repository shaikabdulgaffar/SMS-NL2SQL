// Example JS for simple confirmation on delete
document.addEventListener('DOMContentLoaded', function() {
    const deleteLinks = document.querySelectorAll('a[data-delete]');
    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this record?')) {
                event.preventDefault();
            }
        });
    });
});