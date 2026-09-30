"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
type Target = { id: string; name: string; kind: string; state: string; draining: boolean; runbook: string };
type Alert = { id: string; message: string };
export default function BoardPage() {
  const [rows, setRows] = useState<Target[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [name, setName] = useState("api-west");
  const [kind, setKind] = useState("ok");
  const [error, setError] = useState("");
  async function load() {
    setRows(await api<Target[]>("/targets"));
    setAlerts(await api<Alert[]>("/alerts"));
  }
  useEffect(() => { load().catch((err: Error) => setError(err.message)); }, []);
  return (
    <main>
      <h1>Control board</h1>
      {error ? <p className="err">{error}</p> : null}
      <p className="row">
        <input value={name} onChange={(e) => setName(e.target.value)} />
        <select value={kind} onChange={(e) => setKind(e.target.value)}><option value="ok">ok</option><option value="fail">fail</option></select>
        <button type="button" onClick={() => api("/targets", { method: "POST", body: JSON.stringify({ name, kind }) }).then(load)}>Add target</button>
        <button type="button" onClick={() => api("/targets/tick", { method: "POST" }).then(load)}>Tick probes</button>
      </p>
      {rows.map((t) => (
        <article className="card" key={t.id}>
          <strong className={t.state}>{t.name}</strong> · {t.state} · {t.kind}
          <p className="muted">{t.runbook || "No runbook"}</p>
          <p className="row">
            <button type="button" onClick={() => api(`/targets/${t.id}/drain`, { method: "POST" }).then(load)}>Drain</button>
            <button type="button" onClick={() => api(`/targets/${t.id}/undrain`, { method: "POST" }).then(load)}>Restore</button>
            <button type="button" onClick={() => api(`/targets/${t.id}/runbook`, { method: "POST", body: JSON.stringify({ text: "Page on-call. Fail over to the healthy region." }) }).then(load)}>Attach runbook</button>
          </p>
        </article>
      ))}
      <h2>Alerts</h2>
      {alerts.map((a) => <article className="card" key={a.id}>{a.message}</article>)}
    </main>
  );
}
