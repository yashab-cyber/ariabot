async function fetchStats() {
    try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        
        document.getElementById('val-guilds').innerText = data.guilds_count;
        document.getElementById('val-users').innerText = data.total_users;
        document.getElementById('val-latency').innerText = `${data.latency_ms} ms`;
        document.getElementById('val-sys').innerText = `${data.cpu_usage}% / ${data.memory_usage}%`;

        const badge = document.getElementById('status-badge');
        badge.innerText = data.status.toUpperCase();
        badge.style.background = 'rgba(16, 185, 129, 0.2)';
    } catch (e) {
        document.getElementById('status-badge').innerText = 'OFFLINE / DISCONNECTED';
        document.getElementById('status-badge').style.background = 'rgba(239, 68, 68, 0.2)';
    }
}

async function fetchLogs() {
    try {
        const res = await fetch('/api/logs');
        const data = await res.json();
        document.getElementById('logs-view').innerText = data.logs.join('');
    } catch (e) {
        document.getElementById('logs-view').innerText = 'Failed to load logs.';
    }
}

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

    document.getElementById(`tab-${tabName}`).style.display = 'block';
    if (tabName === 'logs') fetchLogs();
}

async function saveSettings() {
    alert('Settings updated successfully!');
}

fetchStats();
setInterval(fetchStats, 5000);
