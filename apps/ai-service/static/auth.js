// User auth & points system added incrementally (no rewrites).

class AuthService {
    constructor() {
        this.tokenKey = 'uvolution_auth_token';
        this.user = null;
        this.init();
    }

    init() {
        this.checkLogin();
        this.bindEvents();
    }

    async checkLogin() {
        const token = localStorage.getItem(this.tokenKey);
        if (token) {
            try {
                const response = await fetch('/users/me', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.ok) {
                    this.user = await response.json();
                    this.updateUI(true);
                } else {
                    this.logout();
                }
            } catch (e) {
                console.error("Auth check failed", e);
                this.logout();
            }
        } else {
            this.updateUI(false);
        }
    }

    bindEvents() {
        // Login Form
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = document.getElementById('loginEmail').value;
                const password = document.getElementById('loginPassword').value;
                await this.login(email, password);
            });
        }

        // Signup Form
        const signupForm = document.getElementById('signupForm');
        if (signupForm) {
            signupForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = document.getElementById('signupEmail').value;
                const password = document.getElementById('signupPassword').value;
                const name = document.getElementById('signupName').value;
                await this.signup(email, password, name);
            });
        }

        // Logout Button
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        }

        // Social Login Buttons
        const socialBtns = document.querySelectorAll('.social-btn');
        socialBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const provider = btn.getAttribute('data-provider');
                alert(`${provider.charAt(0).toUpperCase() + provider.slice(1)} login is coming soon!`);
            });
        });
    }

    async login(email, password) {
        try {
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const response = await fetch('/auth/login', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem(this.tokenKey, data.access_token);
                $('#loginModal').modal('hide');
                this.checkLogin();
            } else {
                alert('Login failed. Please check your credentials.');
            }
        } catch (e) {
            console.error("Login error", e);
            alert('An error occurred during login.');
        }
    }

    async signup(email, password, name) {
        try {
            const response = await fetch('/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password, name })
            });

            if (response.ok) {
                // Auto login after signup
                await this.login(email, password);
                $('#signupModal').modal('hide');
            } else {
                const data = await response.json();
                alert('Signup failed: ' + (data.detail || 'Unknown error'));
            }
        } catch (e) {
            console.error("Signup error", e);
            alert('An error occurred during signup.');
        }
    }

    async updatePassword(oldPassword, newPassword) {
        try {
            const token = localStorage.getItem(this.tokenKey);
            const response = await fetch('/auth/password', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
            });

            if (response.ok) {
                alert('Password updated successfully!');
                document.getElementById('changePasswordForm').reset();
            } else {
                const data = await response.json();
                alert('Update failed: ' + (data.detail || 'Unknown error'));
            }
        } catch (e) {
            console.error("Password update error", e);
            alert('An error occurred during password update.');
        }
    }

    async deleteAccount() {
        try {
            const token = localStorage.getItem(this.tokenKey);
            const response = await fetch('/auth/me', {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                alert('Account deleted successfully.');
                this.logout();
                window.location.href = '/';
            } else {
                alert('Account deletion failed.');
            }
        } catch (e) {
            console.error("Account deletion error", e);
            alert('An error occurred during account deletion.');
        }
    }

    logout() {
        localStorage.removeItem(this.tokenKey);
        this.user = null;
        this.updateUI(false);
    }

    updateUI(isLoggedIn) {
        const authNav = document.getElementById('auth-nav');
        if (!authNav) return;

        if (isLoggedIn && this.user) {
            authNav.innerHTML = `
                <li>
                    <a href="/customer">
                        <i class="fa fa-user-circle"></i> ${this.user.name}
                    </a>
                </li>
                <li><a href="#" id="logoutBtn">Logout</a></li>
            `;
            // Re-bind logout since DOM changed
            document.getElementById('logoutBtn').addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        } else {
            authNav.innerHTML = `
                <li><a href="#" data-toggle="modal" data-target="#loginModal">Login</a></li>
                <li><a href="#" data-toggle="modal" data-target="#signupModal" class="btn btn-primary btn-sm rounded" style="padding: 5px 15px; color: white;">Sign Up</a></li>
            `;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.authService = new AuthService();
});
