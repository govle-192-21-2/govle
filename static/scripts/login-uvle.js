// Public key for encrypting user UVLê credentials
const govle_public_key = `-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAzcl2yC8opGI7sGpz7PlZ
P4rDIPfRLJW/4a1YMqi0+APH+zN7Ldx2O09YlyL+XJULmjEp/qNct5ekQfs8jXKj
gD52I67WbaAnv81RMJdrZmMZPMv12Iv84PvnEpK8ppGjvEZTzY8Ydofq+camIXcv
YWRBAX2jkKKoC2GZhXtiLWVA5d0Qf06AougQ1wtbnZ79Ri8qt4mXcIlmiEqM0BtX
pz9PBlDJpO7aWHPmSt6JaEu4Mt9DQXctgvnq/dbsPIuxNxq1TndOhGyaj6saeXTK
yp3ponUiSg1rEH6o+CgJ7QK1R8vW7jJ78ZKcoYzEoQnOkfm/yCOdmCQLf8BtGbYP
aqg46brOskQDCwwKiDwkfmbXQ6G9c7fmFAhHOuJntEcF5EIDFayZbsQkL1EcqTEp
5UB72evFowqiOdlZmXYtp9PAmOvNStLfMc8VfFCyXqlUINjAruAZCu3RV8ZXnF43
SwyxbOypTSwazTyvybKj8f7FOXAy23yO3XnXdnZtUqYNhQjQVZFIpXao7mdUgDRQ
QR4epmYL/WecC3n2+qZuY2MUhtkt4swI5kHRRoCEq/OQ2tgZJNPuRuJRfURq8M8O
XFBYdB0RI2q9mkApg9eZ0aPIkaJ81XpOAx9g0VHXzufeyHEHUyzDVQJbc7zrQoln
7urTT9ZlHYPH1WSn527YqVcCAwEAAQ==
-----END PUBLIC KEY-----`;

window.onload = () => {
    // Unhide the form when the "I understand" checkbox is filled
    const checkbox = document.getElementById('exampleCheck1');
    const form = document.querySelector('form');
    const message = document.getElementById('alert-content');
    checkbox.onchange = () => {
        if (checkbox.checked) {
            form.style.display = 'block';
            message.style.display = 'none';
        } else {
            form.style.display = 'none';
            message.style.display = 'block';
        }
    }

    // Form submit handler
    form.addEventListener('submit', (event) => {
        event.preventDefault();

        // Get username and password
        const username = document.getElementById('uvle-username').value;
        const password = document.getElementById('uvle-password').value;

        // Check if either field is empty
        if (username.length === 0 || password.length === 0) {
            alert('Please fill in both fields');
            return;
        }
        
        // Encrypt credentials
        const credentials = `${username}:${password}`;
        const encrypt = new JSEncrypt();
        encrypt.setPublicKey(govle_public_key);
        const encrypted = encrypt.encrypt(credentials);
        
        // Transmit encrypted credentials to server via POST
        fetch('/link-uvle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'credentials': encrypted
            })
        }).then(response => response.json())
            .then(data => {
                if (data['success']) {
                    window.location.href = '/settings';
                } else {
                    alert(data['error']);
                }
            });
    });
}