// itsamha.com: certifications rendering + contact form
const CONTACT_API = 'https://qoc5759x8c.execute-api.us-east-1.amazonaws.com/prod';

document.addEventListener('DOMContentLoaded', () => {
    loadCertifications();
    setupContactForm();
    const year = document.getElementById('year');
    if (year) year.textContent = String(new Date().getFullYear());
});

// certifications.json is generated at build time from Credly
// (scripts/fetch_certifications.py) and deployed with the site.
async function loadCertifications() {
    const grid = document.getElementById('certs-grid');
    if (!grid) return;
    try {
        const resp = await fetch('certifications.json');
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        renderCerts(grid, data.featured || []);
        renderBadges(data.badges || []);
    } catch (err) {
        console.error('Failed to load certifications:', err);
        grid.innerHTML = '<p class="loading">Couldn\'t load certifications. ' +
            'See them on <a href="https://www.credly.com/users/amha-shiferaw" ' +
            'target="_blank" rel="noopener">Credly</a>.</p>';
    }
}

function formatDate(iso) {
    const d = new Date(iso + 'T00:00:00');
    if (isNaN(d)) return iso;
    return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
}

function renderCerts(grid, certs) {
    grid.innerHTML = '';
    for (const cert of certs) {
        const el = document.createElement(cert.url ? 'a' : 'div');
        el.className = 'cert-card';
        if (cert.url) {
            el.href = cert.url;
            el.target = '_blank';
            el.rel = 'noopener';
        }
        const img = document.createElement('img');
        img.src = cert.image;
        img.alt = '';
        img.loading = 'lazy';
        const text = document.createElement('div');
        const name = document.createElement('div');
        name.className = 'cert-name';
        name.textContent = cert.name;
        const meta = document.createElement('div');
        meta.className = 'cert-meta';
        meta.textContent = `${cert.issuer} · ${formatDate(cert.date)}`;
        text.append(name, meta);
        el.append(img, text);
        grid.appendChild(el);
    }
}

function renderBadges(badges) {
    if (!badges.length) return;
    const wrap = document.getElementById('badges-row-wrap');
    const row = document.getElementById('badges-row');
    if (!wrap || !row) return;
    row.innerHTML = '';
    for (const badge of badges) {
        const a = document.createElement('a');
        a.href = badge.url;
        a.target = '_blank';
        a.rel = 'noopener';
        a.title = `${badge.name} (${badge.issuer})`;
        const img = document.createElement('img');
        img.src = badge.image;
        img.alt = badge.name;
        img.loading = 'lazy';
        a.appendChild(img);
        row.appendChild(a);
    }
    wrap.hidden = false;
}

function setupContactForm() {
    const form = document.getElementById('contact-form');
    if (!form) return;
    const status = document.getElementById('form-status');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = form.querySelector('button[type="submit"]');
        const formData = new FormData(form);
        btn.disabled = true;
        status.className = 'form-status';
        status.textContent = 'Sending…';
        try {
            const resp = await fetch(`${CONTACT_API}/contact`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: formData.get('name'),
                    email: formData.get('email'),
                    subject: formData.get('subject') || 'Contact Form Submission',
                    message: formData.get('message'),
                }),
            });
            if (!resp.ok) {
                const body = await resp.json().catch(() => ({}));
                throw new Error(body.error || `HTTP ${resp.status}`);
            }
            status.classList.add('ok');
            status.textContent = 'Thanks, your message was sent.';
            form.reset();
        } catch (err) {
            console.error('Contact form error:', err);
            status.classList.add('err');
            status.textContent = 'Sending failed. Email me directly instead.';
        } finally {
            btn.disabled = false;
        }
    });
}
