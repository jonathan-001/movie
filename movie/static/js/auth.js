// --- Authentication & View Logic ---
let loginView;
let registerView;

/**
 * Custom alert function to display non-blocking messages (instead of alert()).
 */
function alertUser(message) {
    const tempAlert = document.createElement('div');
    tempAlert.className = 'fixed bottom-5 right-5 bg-blue-600 text-white px-4 py-3 rounded-lg shadow-lg z-[9999] transition duration-300 transform translate-y-full';
    tempAlert.textContent = message;
    document.body.appendChild(tempAlert);
    
    // Show alert
    setTimeout(() => {
        tempAlert.style.transform = 'translateY(0)';
    }, 10);

    // Hide and remove alert
    setTimeout(() => {
        tempAlert.style.transform = 'translateY(100%)';
        setTimeout(() => {
            tempAlert.remove();
        }, 300);
    }, 3000);
}

/**
 * Switches the displayed form to the Login view.
 */
function showLoginView(event) {
    if (event) event.preventDefault();
    if (loginView && registerView) {
        loginView.classList.remove('hidden');
        registerView.classList.add('hidden');
    }
}

/**
 * Switches the displayed form to the Register view.
 */
function showRegisterView(event) {
    if (event) event.preventDefault();
    if (loginView && registerView) {
        registerView.classList.remove('hidden');
        loginView.classList.add('hidden');
    }
}

/**
 * Handles the Login form submission (simulated).
 */
function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('login-email').value;
    
    // Basic validation
    if (!email || !document.getElementById('login-password').value) {
        alertUser("Please enter both email and password.");
        return;
    }
    
    // Placeholder for actual authentication API call (e.g., Firebase)
    alertUser('Login functionality simulated for: ' + email);
}

/**
 * Handles the Register form submission (simulated).
 */
function handleRegister(event) {
    event.preventDefault();
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;

    if (password !== confirmPassword) {
        alertUser("Passwords do not match!");
        return;
    }
    
    // Check if the required fields have content before proceeding with simulation
    if (!name || !email || !password) {
        alertUser("Please fill out all fields.");
        return;
    }

    console.log("Attempting to register with:", name, email);
    alertUser('Registration simulated for: ' + name);
    
    // Wait a moment, then switch to the login view
    setTimeout(showLoginView, 500); 
}

document.addEventListener('DOMContentLoaded', () => {
    // 1. Assign view elements
    loginView = document.getElementById('login-view');
    registerView = document.getElementById('register-view');

    // 2. Set initial view
    if (loginView) {
        showLoginView();
    }
    
    // 3. Add listeners for view switching links
    // The "Register" link on the Login form
    document.getElementById('register-link')?.addEventListener('click', (e) => {
        e.preventDefault();
        showRegisterView();
    });

    // The "Login now" link on the Register form
    document.getElementById('login-link')?.addEventListener('click', (e) => {
        e.preventDefault();
        showLoginView();
    });

    // 4. Add listeners for form submissions
    document.querySelector('#login-view form')?.addEventListener('submit', handleLogin);
    document.querySelector('#register-view form')?.addEventListener('submit', handleRegister);
});
