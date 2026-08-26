import React, { useState } from "react";

function Login({ onLogin }) {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");


  // =========================
  // LOGIN
  // =========================

  const login = async () => {

    if (!username || !password) {
      alert("Please enter username and password.");
      return;
    }

    try {

      const response = await fetch(
        "http://localhost:8000/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            username,
            password
          })
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        alert(data.message || "Login failed");
        return;
      }

      // Save logged-in user
      localStorage.setItem(
        "user_id",
        data.user_id
      );

      localStorage.setItem(
        "username",
        data.username
      );

      // Go to Chat
      onLogin(data);

    } catch (error) {

      console.error(error);

      alert("Could not connect to server.");
    }
  };


  // =========================
  // REGISTER
  // =========================

  const register = async () => {

    if (!username || !password) {
      alert("Please enter username and password.");
      return;
    }

    try {

      const response = await fetch(
        "http://localhost:8000/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            username,
            password
          })
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        alert(data.message || "Registration failed");
        return;
      }

      alert(
        "Registration successful! You can now login."
      );

      // Clear password after registration
      setPassword("");

    } catch (error) {

      console.error(error);

      alert("Could not connect to server.");
    }
  };


  // =========================
  // UI
  // =========================

  return (
    <div>

      <h1>AI Job Assistant</h1>

      <h2>Login</h2>

      <input
        placeholder="Username"
        value={username}
        onChange={(e) =>
          setUsername(e.target.value)
        }
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) =>
          setPassword(e.target.value)
        }
      />

      <button onClick={login}>
        Login
      </button>

      <button onClick={register}>
        Create Account
      </button>

    </div>
  );
}

export default Login;