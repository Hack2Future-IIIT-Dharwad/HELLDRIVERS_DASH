document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');

    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(uploadForm);
        const file = formData.get('file');

        console.log('File selected:', file.name);

        try {
            const response = await fetch('https://api.example.com/upload', { // Replace with your API URL
                method: 'POST',
                body: formData
            });

            console.log('Response received', response);

            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            const data = await response.json();
            console.log('Response data', data);
            alert('File uploaded successfully!');
        } catch (error) {
            console.error('There has been a problem with your fetch operation:', error);
            alert('File upload failed. Please try again.');
        }
    });
});
