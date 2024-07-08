async function submitData() {
    const formData = {
        name: document.getElementById('name').value,
        date: document.getElementById('date').value,
        time: document.getElementById('time').value,
        item: document.getElementById('item').value,
        quantity: parseInt(document.getElementById('quantity').value),
        payment: parseFloat(document.getElementById('payment').value),
        role: document.getElementById('role').value,
        location: 'Canteen'
    };

    try {
        const tokenResponse = await fetch('http://127.0.0.1:8080/api/token');
        if (tokenResponse.status === 200) {
            const tokenData = await tokenResponse.json();
            const token = tokenData.token;

            const response = await fetch('http://127.0.0.1:8080/api/purchase', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });

            if (response.status === 200) {
                alert('Data submitted successfully!');
                document.getElementById('purchase-form').reset();
            } else {
                alert(`Failed to submit data: ${response.status}`);
            }
        } else {
            alert(`Failed to get token: ${tokenResponse.status}`);
        }
    } catch (error) {
        alert(`Error connecting to server: ${error}`);
    }
}
