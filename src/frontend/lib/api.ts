export function saveToken(token: string): void { localStorage.setItem("access", token); }
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  if (init.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  const access = localStorage.getItem("access");
  if (access) headers.set("Authorization", `Bearer ${access}`);
  const res = await fetch(`/api${path}`, { ...init, headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message ?? "request failed");
  return data as T;
}
