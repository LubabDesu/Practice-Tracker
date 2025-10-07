// API helper to send cookies

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
    const res = await fetch(path, {
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
