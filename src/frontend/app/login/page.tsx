"use client";
import { useState } from "react";
import { api, saveToken } from "@/lib/api";
export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("password1");
  const [error, setError] = useState("");
  async function send(path: string) {
    const body = await api<{ access_token: string }>(path, { method: "POST", body: JSON.stringify({ email, password }) });
    saveToken(body.access_token);
    window.location.href = "/board";
  }
  return (
    <div className="auth">
      <form className="card" onSubmit={(e) => { e.preventDefault(); send("/auth/sign-in").catch((err: Error) => setError(err.message)); }}>
        <h1>Pulse</h1>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        {error ? <p className="err">{error}</p> : null}
        <p><button type="submit">Sign in</button> <button type="button" onClick={() => send("/auth/sign-up").catch((err: Error) => setError(err.message))}>Sign up</button></p>
      </form>
    </div>
  );
}
