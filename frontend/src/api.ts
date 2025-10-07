// API helper to send cookies
const BASE = import.meta.env.VITE_API_BASE_URL || "";
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
    const res = await fetch(BASE + path, {
        credentials: "include", // include cookies for auth
        headers: {
            "Content-Type": "application/json",
            ...(init.headers || {}),
        },
        ...init,
    });
    if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
    return res.json() as Promise<T>;
}
