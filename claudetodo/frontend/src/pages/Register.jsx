import { useState } from 'react';
import './Register.css';

function Register({ onSwitch }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data.detail || 'Registration failed. Please try again.');
        return;
      }
      onSwitch();
    } catch {
      setError('Network error. Please try again.');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2 className="auth-title">Create Account</h2>
        <form className="auth-form" onSubmit={handleSubmit}>
          <label className="auth-label" htmlFor="reg-email">Email</label>
          <input
            id="reg-email"
            className="auth-input"
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <label className="auth-label" htmlFor="reg-password">Password</label>
          <input
            id="reg-password"
            className="auth-input"
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p className="auth-error">{error}</p>}
          <button className="auth-btn" type="submit">Create Account</button>
        </form>
        <p className="auth-switch">
          Already have an account?{' '}
          <button className="auth-link-btn" type="button" onClick={onSwitch}>
            Login instead
          </button>
        </p>
      </div>
    </div>
  );
}

export default Register;
