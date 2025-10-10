// Load everything when the page is ready
window.addEventListener("DOMContentLoaded", () => {
    // function calls
    fetchtrending();
    fetchredommended();
    fetchwatchlist();
    document.addEventListener("click", async (e) => {
  if (e.target.closest(".dropdown-menu div")) {
    const option = e.target.closest(".dropdown-menu div");
    const cardInner = option.closest(".flip-card-inner");
    const title = cardInner.querySelector(".flip-card-front").textContent.trim();
    const action = option.textContent.trim();

    try {
      const response = await fetch("http://127.0.0.1:5000/update-drama", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, action })
      });

      if (response.ok) {
        console.log(`Success: ${title} -> ${action}`);
      } else {
        console.error("Server said nope:", response.status);
      }
    } catch (err) {
      console.error("Network meltdown:", err);
    }
  }
});

});
// trending
async function fetchtrending() {
    try {
        const res = await fetch("http://127.0.0.1:5000/trending");
        // alert('xffg');
        const data = await res.json();
        if (data.status === "ok") {
            const container = document.querySelectorAll(".cards-container");
            const current_query = container[0]
            current_query.innerHTML = ""; // Clear old cards
            data.trending.forEach(drama => {
                const card = document.createElement("div");
                card.classList.add("card");
                card.innerHTML = `
        <div class="flip-card-inner">
            <div class="flip-card-front">${drama.title}</div>
            <div class="flip-card-back">
            <div class="info">
                <div class="year">${drama.year}</div>
                <details class="option-wrapper">
                <summary class="option">Add</summary>
                <div class="dropdown-menu">
                    <div>Add to Watchlist</div>
                    <div>Mark as Watched</div>
                    <div>Mark as Wish</div>
                </div>
                </details>
                <div class="episodes">Episodes: ${drama.episodes}</div>
                <div class="platform">${drama.platform}</div>
                <div class="description">${drama.description}</div>
            </div>
            </div>
        </div>`;
                current_query.appendChild(card);
            });
        } else {
            alert(data.message || "No trending dramas found.");
        }
    } catch (err) {
        console.error("Error fetching trending:", err);
        alert("Error fetching trending:", err)
    }
}

async function fetchredommended() {
    try {
        const res = await fetch("http://127.0.0.1:5000/recommendations");
        const data = await res.json();
        
        if (data.status === "ok") {
            const container = document.querySelectorAll(".cards-container");
            const current_query = container[2]
            current_query.innerHTML = ""; // Clear old cards
            // alert('xffg');
            data.recommendations.forEach(drama => {
                const card = document.createElement("div");
                card.classList.add("card");
                card.innerHTML = `
        <div class="flip-card-inner">
            <div class="flip-card-front">${drama.title}</div>
            <div class="flip-card-back">
            <div class="info">
                <div class="year">${drama.year}</div>
                <details class="option-wrapper">
                <summary class="option">Add</summary>
                <div class="dropdown-menu">
                    <div>Add to Watchlist</div>
                    <div>Mark as Watched</div>
                    <div>Mark as Wish</div>
                </div>
                </details>
                <div class="episodes">Episodes: ${drama.episodes}</div>
                <div class="platform">${drama.platform}</div>
                <div class="description">${drama.description}</div>
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
        alert("Error fetching recommendations:", err)
    }
}

async function fetchwatchlist() {
    try {
        const res = await fetch("http://127.0.0.1:5000/watchlistexplore");
        const data = await res.json();
        
        if (data.status === "ok") {
            const container = document.querySelectorAll(".cards-container");
            const current_query = container[1]
            current_query.innerHTML = ""; // Clear old cards
            // alert('xffg');
            data.watchlist.forEach(drama => {
                const card = document.createElement("div");
                card.classList.add("card");
                card.innerHTML = `
        <div class="flip-card-inner">
            <div class="flip-card-front">${drama.title}</div>
            <div class="flip-card-back">
            <div class="info">
                <div class="year">${drama.year}</div>
                <details class="option-wrapper">
                <summary class="option">Add</summary>
                <div class="dropdown-menu">
                    <div>Add to Watchlist</div>
                    <div>Mark as Watched</div>
                    <div>Mark as Wish</div>
                </div>
                </details>
                <div class="description">${drama.description}</div>
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
        alert("Error fetching recommendations:", err)
    }
}
