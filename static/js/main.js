// ============================================================
// EVENTLY - Main JavaScript
// ============================================================

// Password strength validation on register
document.addEventListener('DOMContentLoaded', function () {

    // Role tab switcher on register page
    window.setRole = function(role, btn) {
        document.querySelectorAll('.role-tabs button').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const roleField = document.querySelector('#id_role');
        if (roleField) roleField.value = role;
    };

    // Password strength indicator
    const passwordField = document.querySelector('#id_password1');
    if (passwordField) {
        const indicator = document.createElement('div');
        indicator.id = 'password-strength';
        indicator.style.cssText = 'margin-top:6px;font-size:12px;font-weight:600;';
        passwordField.parentNode.appendChild(indicator);

        passwordField.addEventListener('input', function () {
            const val = this.value;
            let strength = 0;
            if (val.length >= 8) strength++;
            if (/[A-Z]/.test(val)) strength++;
            if (/[0-9]/.test(val)) strength++;
            if (/[^A-Za-z0-9]/.test(val)) strength++;

            const labels = ['', 'Weak', 'Fair', 'Good', 'Strong'];
            const colors = ['', '#e8342a', '#f59e0b', '#3b82f6', '#28a745'];
            indicator.textContent = val.length > 0 ? 'Password strength: ' + labels[strength] : '';
            indicator.style.color = colors[strength];
        });
    }

    // Password match check
    const password2Field = document.querySelector('#id_password2');
    if (password2Field) {
        const matchMsg = document.createElement('div');
        matchMsg.style.cssText = 'margin-top:6px;font-size:12px;font-weight:600;';
        password2Field.parentNode.appendChild(matchMsg);

        password2Field.addEventListener('input', function () {
            const p1 = document.querySelector('#id_password1').value;
            const p2 = this.value;
            if (p2.length === 0) {
                matchMsg.textContent = '';
            } else if (p1 === p2) {
                matchMsg.textContent = '✓ Passwords match';
                matchMsg.style.color = '#28a745';
            } else {
                matchMsg.textContent = '✗ Passwords do not match';
                matchMsg.style.color = '#e8342a';
            }
        });
    }

    // Auto-dismiss messages after 4 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(function (msg) {
        setTimeout(function () {
            msg.style.transition = 'opacity 0.5s';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500);
        }, 4000);
    });

    // Confirm delete actions
    const deleteForms = document.querySelectorAll('form[data-confirm]');
    deleteForms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            if (!confirm(form.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

});