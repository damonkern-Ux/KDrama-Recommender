// Load everything when the page is ready
window.addEventListener("DOMContentLoaded", () => {
    // function calls
    fetchwatchedlist();
});

async function fetchwatchedlist() {
    try {
        const res = await fetch("http://127.0.0.1:5000/watchedlist");
        const data = await res.json();
        
        if (data.status === "ok") {
            const container = document.querySelectorAll(".cards-container");
            const current_query = container[0]
            current_query.innerHTML = ""; // Clear old cards
            data.watched.forEach(drama => {
                const card = document.createElement("div");
                card.classList.add("card");
                card.innerHTML = `
        <div class="flip-card-inner">
            <div class="flip-card-front">${drama.title}</div>
            <div class="flip-card-back">
            <div class="info">
                <div class="year">${drama.year}</div>
                <div class="episodes">${drama.episode} Episodes</div>
                <div class="date">Added on ${drama.time}</div>
            </div>
            </div>
        </div>`;
                current_query.appendChild(card);
            });
        } else {
            alert(data.message || "No trending dramas found.");
        }
    } catch (err) {
        console.error("Error fetching recommendations:", err);
        alert("Error fetching recommendations")
    }
}