window.addEventListener("DOMContentLoaded", async () => {

    try {
        const res = await fetch("http://127.0.0.1:5000/profile");
        const data = await res.json();
        console.log(data);
        if (data.status === "ok") {
            fetchwatchednumber(data);
            fetchwatchedcard(data);
        } else {
            console.error("Server error:", data);
        }
    } catch (err) {
        console.error("Fetch failed:", err);
    }
});

function fetchwatchednumber(data) {
    const container = document.querySelectorAll(".stat-holder");
    const current_query = container[0];
    current_query.innerHTML = ""; // Clear old cards
    const card = document.createElement("div");
    card.classList.add("stat-card");
    card.innerHTML = `
        <h4 class="stat-label">Current Status</h4>
        <div class="status">Binge Watcher 10/10</div>
        <div class="status">Drama Devotee 10/10</div>
        <div class="next-status">
          <div class="next-achievement">K Drama Addict.</div>
          <div class="progress">7/10</div>
          <div class="progress-bar" style="width: 70%;"></div>
        </div>`;
    current_query.appendChild(card);
}

function fetchwatchedcard(data) {
    const container = document.querySelectorAll(".stat-holder");
    const current_query = container[0];

    const card1 = document.createElement("div");
    card1.classList.add("stat-card");
    card1.innerHTML = `
        <h4 class="stat-label">Watched</h4>
        <h1 class="stat-number">${data.watched.watched}</h1>`;
    current_query.appendChild(card1);

    const card2 = document.createElement("div");
    card2.classList.add("stat-card");
    card2.innerHTML = `
        <h4 class="stat-label">Watch List</h4>
        <h1 class="stat-number">${data.watched.watch}</h1>`;
    current_query.appendChild(card2);

    const card3 = document.createElement("div");
    card3.classList.add("stat-card");
    card3.innerHTML = `
        <h4 class="stat-label">Wish List</h4>
        <h1 class="stat-number">${data.watched.wish}</h1>`;
    current_query.appendChild(card3);

    const card4 = document.createElement("div");
    card4.classList.add("stat-card");
    // fetch data from local storage
    card4.innerHTML = `
        <h4 class="stat-label">Preferred Genres</h4>
        <div class="tag-container">
          <span class="tag">Romance</span>
          <span class="tag">Thriller</span>
          <span class="tag">Comedy</span>
          <span class="tag">Fantasy</span>
          <span class="tag">Crime</span>
          <span class="tag">Sci-Fi</span>
        </div>`;
    current_query.appendChild(card4);

    const card5 = document.createElement("div");
    card5.classList.add("stat-card");
    // fetch from local storage
    card5.innerHTML = `
       <h4 class="stat-label">Favourite Actors</h4>
        <div class="actor-list">
          <span class="actor">Song Kang</span>
          <span class="actor">Song Joong Ki</span>
          <span class="actor">Kim Soo-hyun</span>
        </div>
        `;
    current_query.appendChild(card5);

    const card6 = document.createElement("div");
    card6.classList.add("stat-card");
    card6.innerHTML = `
        <h4 class="stat-label">Favourite Actresses</h4>
        <div class="actor-list">
          <span class="actor">Kim Yoo Jung</span>
          <span class="actor">Park Shin-hye</span>
          <span class="actor">Seo Yea Ji</span>
        </div>
        `;
    current_query.appendChild(card6);

    const card7 = document.createElement("div");
    card7.classList.add("stat-card");
    card7.innerHTML = `
<h4 class="stat-label">Preferred Platforms</h4>
        <div class="tag-container">
            <span class="tag">Netflix</span>
            <span class="tag">Prime</span>
            <span class="tag">Viki</span>
            <span class="tag">Apple TV+</span>
        </div>
        `;
    current_query.appendChild(card7);
}
