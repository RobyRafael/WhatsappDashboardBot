document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const mediaInput = document.getElementById('media-input');
    const messageInput = document.getElementById('message-input');
    const recipientInput = document.getElementById('recipient-input');
    const submitButton = document.getElementById('submit-button');
    const notificationArea = document.getElementById('notification-area');

    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(uploadForm);

        fetch('/api/media/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                notificationArea.innerHTML = 'Media uploaded successfully!';
            } else {
                notificationArea.innerHTML = 'Error uploading media.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            notificationArea.innerHTML = 'Error uploading media.';
        });
    });

    submitButton.addEventListener('click', function() {
        const message = messageInput.value;
        const recipient = recipientInput.value;

        fetch('/api/messages/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message, recipient })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                notificationArea.innerHTML = 'Message sent successfully!';
            } else {
                notificationArea.innerHTML = 'Error sending message.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            notificationArea.innerHTML = 'Error sending message.';
        });
    });
});