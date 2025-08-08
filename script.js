// Configuration
const CONFIG = {
    apiGatewayUrl: 'https://qoc5759x8c.execute-api.us-east-1.amazonaws.com/prod'
};

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadPortfolioData();
});

// Initialize application
function initializeApp() {
    // Setup smooth scrolling
    setupSmoothScrolling();
}

// Setup event listeners
function setupEventListeners() {
    // Contact form submission
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactForm);
    }
    
    // Auth button removed
    
    // Navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Setup smooth scrolling for hero buttons
function setupSmoothScrolling() {
    const heroButtons = document.querySelectorAll('.hero-buttons .btn');
    heroButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// Load portfolio data from API
async function loadPortfolioData() {
    try {
        const response = await fetch(`${CONFIG.apiGatewayUrl}/portfolio`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Render projects
        renderProjects(data.projects);
        
        // Render skills
        renderSkills(data.skills);
        
        // Render certifications
        renderCertifications(data.certifications);
        
    } catch (error) {
        console.error('Error loading portfolio data:', error);
        
        // Fallback to static data
        loadFallbackData();
    }
}

// Load fallback data if API fails
function loadFallbackData() {
    const fallbackProjects = [
        {
            id: 1,
            title: 'Personal Cloud Portfolio Website',
            description: 'This very website - a complete AWS cloud architecture showcase',
            technologies: ['Terraform', 'S3', 'CloudFront', 'Route 53', 'Lambda', 'API Gateway', 'VPC'],
            highlights: [
                'Complete Infrastructure as Code with Terraform',
                'Serverless architecture with Lambda and API Gateway',
                'Global CDN with CloudFront and custom domain',
                'Cost-optimized design (~$5/month)',
                'Responsive design with modern CSS'
            ]
        },
        {
            id: 2,
            title: 'FireFerral',
            description: 'A modern web application for managing referrals and connections',
            technologies: ['React', 'Firebase', 'JavaScript', 'CSS', 'Web App'],
            highlights: [
                'Modern responsive web application',
                'Firebase backend integration',
                'User-friendly referral management system',
                'Deployed on Firebase hosting'
            ],
            url: 'https://fireferral.web.app'
        }
    ];
    
    const fallbackSkills = {
        'cloud_platforms': ['AWS', 'Azure', 'Google Cloud'],
        'infrastructure': ['Terraform', 'CloudFormation', 'Ansible'],
        'containers': ['Docker', 'Kubernetes', 'EKS', 'ECS'],
        'monitoring': ['CloudWatch', 'Prometheus', 'Grafana']
    };
    
    renderProjects(fallbackProjects);
    renderSkills(fallbackSkills);
    
    // Fallback certifications
    const fallbackCertifications = [
        {
            name: 'AWS Certified Solutions Architect - Associate',
            issuer: 'Amazon Web Services',
            date: 'August 2025',
            credly_url: 'https://www.credly.com/users/amha-shiferaw'
        },
        {
            name: 'AWS Certified Cloud Practitioner',
            issuer: 'Amazon Web Services',
            date: 'May 2025',
            credly_url: 'https://www.credly.com/users/amha-shiferaw'
        }
    ];
    renderCertifications(fallbackCertifications);
}

// Render projects
function renderProjects(projects) {
    const projectsGrid = document.getElementById('projects-grid');
    if (!projectsGrid) return;
    
    projectsGrid.innerHTML = '';
    
    projects.forEach(project => {
        const projectCard = document.createElement('div');
        projectCard.className = 'project-card';
        
        const techTags = project.technologies.map(tech => 
            `<span class="tech-tag">${tech}</span>`
        ).join('');
        
        const highlights = project.highlights.map(highlight => 
            `<li>${highlight}</li>`
        ).join('');
        
        const projectLink = project.url ? `<a href="${project.url}" target="_blank" class="project-link">View Project →</a>` : '';
        
        projectCard.innerHTML = `
            <h3>${project.title}</h3>
            <p>${project.description}</p>
            <div class="project-tech">
                ${techTags}
            </div>
            <ul class="project-highlights">
                ${highlights}
            </ul>
            ${projectLink}
        `;
        
        projectsGrid.appendChild(projectCard);
    });
}

// Render skills
function renderSkills(skills) {
    const skillsContent = document.getElementById('skills-content');
    if (!skillsContent) return;
    
    skillsContent.innerHTML = '';
    
    Object.entries(skills).forEach(([category, skillList]) => {
        const skillCategory = document.createElement('div');
        skillCategory.className = 'skill-category';
        
        const skillTags = skillList.map(skill => 
            `<span class="skill-tag">${skill}</span>`
        ).join('');
        
        skillCategory.innerHTML = `
            <h3>${category.replace('_', ' ')}</h3>
            <div class="skill-tags">
                ${skillTags}
            </div>
        `;
        
        skillsContent.appendChild(skillCategory);
    });
}

// Handle contact form submission
async function handleContactForm(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    const contactData = {
        name: formData.get('name'),
        email: formData.get('email'),
        subject: formData.get('subject') || 'Contact Form Submission',
        message: formData.get('message')
    };
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${CONFIG.apiGatewayUrl}/contact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(contactData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Success
            alert('Thank you for your message! I will get back to you soon.');
            form.reset();
        } else {
            // Error
            alert(`Error: ${result.error || 'Failed to send message'}`);
        }
        
    } catch (error) {
        console.error('Error sending contact form:', error);
        alert('Failed to send message. Please try again later.');
    } finally {
        // Reset button state
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// Authentication functions removed

// OAuth functions removed

// Render certifications
function renderCertifications(certifications) {
    const certificationsContent = document.getElementById('certifications-content');
    if (!certificationsContent) return;
    
    certificationsContent.innerHTML = '';
    
    certifications.forEach(cert => {
        const certCard = document.createElement('div');
        certCard.className = 'certification-card';
        
        certCard.innerHTML = `
            <h3>${cert.name}</h3>
            <div class="issuer">${cert.issuer}</div>
            <div class="date">Earned: ${cert.date}</div>
            <a href="${cert.credly_url}" target="_blank" class="credential">
                View on Credly
            </a>
        `;
        
        certificationsContent.appendChild(certCard);
    });
}

// Check if we're on the callback page
if (window.location.pathname === '/callback') {
    handleOAuthCallback();
}