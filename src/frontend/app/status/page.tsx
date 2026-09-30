"use client";
import { useEffect, useState } from "react";
type Snap = { status: string; services: { name: string; state: string; runbook: string }[] };
export default function StatusPage() {
  const [snap, setSnap] = useState<Snap>({ status: "operational", services: [] });
  useEffect(() => { fetch("/api/status").then((r) => r.json()).then(setSnap).catch(() => null); }, []);
  return (
    <main>
      <h1 className={snap.status === "operational" ? "healthy" : "down"}>{snap.status}</h1>
      {snap.services.map((s) => (
        <article className="card" key={s.name}>
          <strong className={s.state}>{s.name}</strong> · {s.state}
          {s.runbook ? <p className="muted">{s.runbook}</p> : null}
        </article>
      ))}
    </main>
  );
}
