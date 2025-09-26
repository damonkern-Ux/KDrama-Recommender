document.querySelector(".button1").addEventListener("click", function() {
    const username = document.querySelector(".textbox[type='text']").value;
    const password = document.querySelector(".textbox[type='password']").value;

    // Alert the user that data is being collected
    alert(`Collecting Data:\nUsername: ${username}\nPassword: ${password}`);

    // Send data to server
    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    })
    .then((res) => res.json())
    .then((data) => {
        if (data.status === "ok") {
        alert("Login successful!");
        window.location.href = "explore.html"; // redirect after success
        } 
        else {
        alert("Login failed: " + data.message);
        }
    })
    .catch(err => {
        console.error("Error:", err);
        alert("Something went wrong. Check console.");
    });
});
