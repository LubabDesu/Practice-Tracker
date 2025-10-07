import { useEffect, useState } from "react";

type Stats = {
    total_minutes_last_7_days: number;
    top_piece_last_7_days: string | null;
    current_streak_days: number;
};

export default function StatsPanel({ refresh = 0 }: { refresh?: number }) {
    const [stats, setStats] = useState<Stats | null>(null);

    useEffect(() => {
        (async () => {
            const res = await fetch("/api/stats/overview", {
                credentials: "include",
            });
            if (!res.ok) throw new Error(await res.text());
            setStats(await res.json());
        })().catch(() => setStats(null));
    }, [refresh]);

    if (!stats) return <p>Loading stats…</p>;
    return (
        <section>
            <h2>Stats</h2>
            <p>Streak: 🔥 {stats.current_streak_days} day(s)</p>
            <p>Minutes (7d): {stats.total_minutes_last_7_days}</p>
            <p>Top piece (7d): {stats.top_piece_last_7_days || "—"}</p>
        </section>
    );
}
