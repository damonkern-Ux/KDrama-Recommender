// --- Dropdown action handler ---
document.addEventListener('click', async (e) => {
  const option = e.target.closest('.dropdown-menu div');
  if (!option) return; // not a dropdown click

  const cardInner = option.closest('.flip-card-inner');
  if (!cardInner) return

  const title = cardInner.querySelector('.flip-card-front').textContent.trim();
  const action = option.textContent.trim();

  try {
    const response = await fetch('http://127.0.0.1:5000/update-drama', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, action })
    });

    if (response.ok) {
      console.log(`Success: ${title} -> ${action}`);
    } else {
      console.error('Server said nope:', response.status);
    }
  } catch (err) {
    console.error('Network meltdown:', err);
  }
});

// --- Search box handler ---
const searchBox = document.querySelector('.textbox');

searchBox.addEventListener('keypress', async (e) => {
  if (e.key !== 'Enter') return;

  const query = searchBox.value.trim();
  if (!query) return;

  try {
    const response = await fetch('http://127.0.0.1:5000/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });

    if (!response.ok) throw new Error(`HTTP error ${response.status}`);

    const data = await response.json();
    console.log('Response from server:', data);

    if (data.status === 'ok' && Array.isArray(data.search)) {
      const container = document.querySelector('.cards-container');
      container.innerHTML = ''; // clear old cards

      data.search.forEach(drama => {
        const card = document.createElement('div');
        card.classList.add('card');
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
        container.appendChild(card);
      });
    } else {
      alert(data.message || 'No dramas found.');
    }
  } catch (err) {
    console.error('Search failed:', err);
    alert('Server didn’t respond. Check console.');
  }
});
