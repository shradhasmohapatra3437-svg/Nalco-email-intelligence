import { useState, useEffect } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, ResponsiveContainer } from "recharts";
import "./App.css";

const API = "http://127.0.0.1:8000";
const CATEGORIES = ["All", "Finance", "HR", "Systems/IT", "Procurement", "Operations", "Legal/Vigilance", "Administration", "Safety/Environment", "Friends/Family", "Others"];
const URGENCY_COLORS = { High: "#ef4444", Medium: "#f59e0b", Low: "#22c55e" };
const PIE_COLORS = ["#ef4444", "#f59e0b", "#22c55e"];

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    setError("");
    try {
      const form = new FormData();
      form.append("username", username);
      form.append("password", password);
      const res = await axios.post(`${API}/login`, form);
      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("role", res.data.role);
      onLogin(res.data.role);
    } catch (err) {
      setError("Invalid username or password");
    }
    setLoading(false);
  };

  return (
    <div className="login-page">
      <div className="login-box">
        <div className="login-logo">📧</div>
        <h1>NALCO Mail Intelligence</h1>
        <p className="login-subtitle">Internal Email Intelligence System</p>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleLogin()}
        />
        {error && <p className="error">{error}</p>}
        <button onClick={handleLogin} disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
        <p className="login-hint">Admin: admin / admin123 | Employee: employee / emp123</p>
      </div>
    </div>
  );
}

function Analytics({ emails }) {
  const categoryData = CATEGORIES.slice(1).map(cat => ({
    name: cat.length > 10 ? cat.substring(0, 10) + ".." : cat,
    count: emails.filter(e => e.category === cat).length
  })).filter(d => d.count > 0);

  const urgencyData = ["High", "Medium", "Low"].map(u => ({
    name: u,
    value: emails.filter(e => e.urgency === u).length
  })).filter(d => d.value > 0);

  return (
    <div className="analytics">
      <div className="chart-box">
        <h4>Emails by Category</h4>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={categoryData}>
            <XAxis dataKey="name" tick={{ fontSize: 11 }} />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="chart-box">
        <h4>Urgency Distribution</h4>
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie data={urgencyData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={70} label={({ name, value }) => `${name}: ${value}`}>
              {urgencyData.map((_, i) => <Cell key={i} fill={PIE_COLORS[i]} />)}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function Dashboard({ role, onLogout }) {
  const [emails, setEmails] = useState([]);
  const [selected, setSelected] = useState(null);
  const [category, setCategory] = useState("All");
  const [view, setView] = useState("inbox");
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem("token");

  useEffect(() => {
    axios.get(`${API}/emails`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => { setEmails(res.data); setLoading(false); })
      .catch(() => { setLoading(false); onLogout(); });
  }, []);

  const filtered = category === "All" ? emails : emails.filter(e => e.category === category);

  return (
    <div className="app">
      <div className="sidebar">
        <h2>NALCO Mail Intelligence</h2>
        <div className="user-info">
          <span>👤 {role === "admin" ? "Admin" : "Employee"}</span>
          <button className="logout-btn" onClick={onLogout}>Logout</button>
        </div>
        <div className="view-toggle">
          <button className={view === "inbox" ? "active" : ""} onClick={() => setView("inbox")}>Inbox</button>
          <button className={view === "analytics" ? "active" : ""} onClick={() => setView("analytics")}>Analytics</button>
        </div>
        {view === "inbox" && (
          <ul>
            {CATEGORIES.map(cat => (
              <li key={cat} className={category === cat ? "active" : ""} onClick={() => setCategory(cat)}>
                {cat}
                <span className="count">{cat === "All" ? emails.length : emails.filter(e => e.category === cat).length}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {view === "analytics" ? (
        <div className="analytics-page">
          <h3>Email Analytics</h3>
          <p className="meta">{emails.length} emails processed</p>
          <Analytics emails={emails} />
        </div>
      ) : (
        <>
          <div className="email-list">
            {loading ? <p>Loading...</p> : filtered.length === 0 ? <p className="empty">No emails found.</p> : filtered.map(email => (
              <div key={email.id} className={`email-card ${selected?.id === email.id ? "selected" : ""}`} onClick={() => setSelected(email)}>
                <div className="email-header">
                  <span className="sender">{email.sender.split("<")[0].trim()}</span>
                  <span className="urgency-badge" style={{ backgroundColor: URGENCY_COLORS[email.urgency] }}>{email.urgency}</span>
                </div>
                <div className="subject">{email.subject}</div>
                <div className="category-tag">{email.category}</div>
              </div>
            ))}
          </div>

          <div className="email-detail">
            {selected ? (
              <>
                <h3>{selected.subject}</h3>
                <p className="meta">From: {selected.sender}</p>
                <p className="meta">Category: {selected.category} | Urgency: <span style={{ color: URGENCY_COLORS[selected.urgency] }}>{selected.urgency}</span></p>
                <div className="summary-box">
                  <h4>AI Summary</h4>
                  <p>{selected.summary}</p>
                </div>
                <div className="body-preview">
                  <h4>Email Preview</h4>
                  <p>{selected.body_preview}</p>
                </div>
                <a href="https://gmail.com" target="_blank" rel="noreferrer" className="gmail-btn">Open Gmail →</a>
              </>
            ) : (
              <p className="placeholder">Select an email to view details</p>
            )}
          </div>
        </>
      )}
    </div>
  );
}

function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem("token"));
  const [role, setRole] = useState(localStorage.getItem("role") || "");

  const handleLogin = (userRole) => {
    setRole(userRole);
    setLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    setLoggedIn(false);
    setRole("");
  };

  return loggedIn ? <Dashboard role={role} onLogout={handleLogout} /> : <Login onLogin={handleLogin} />;
}

export default App;


