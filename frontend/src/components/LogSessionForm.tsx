import { useEffect, useState } from "react";
import { api } from "../api";

type Piece = { id: number; title: string; composer?: string | null };

export default function LogSessionForm({ onSaved }: { onSaved: () => void }) {
    const [pieces, setPieces] = useState<Piece[]>([]);
    const [pieceId, setPieceId] = useState<number | "">("");
    const [practiceDate, setPracticeDate] = useState<string>(() =>
        new Date().toISOString().slice(0, 10)
    );
    const [minutes, setMinutes] = useState<number>(30);
    const [focus, setFocus] = useState<string>("");
    const [notes, setNotes] = useState<string>("");

    useEffect(() => {
        api<Piece[]>("/api/pieces").then(setPieces);
    }, []);

    async function submit(e: React.FormEvent) {
        e.preventDefault();
        if (!pieceId) return;
        await api("/api/sessions", {
            method: "POST",
            body: JSON.stringify({
                piece_id: Number(pieceId),
                practice_date: practiceDate,
                minutes: Number(minutes),
                focus: focus || null,
                notes: notes || null,
            }),
        });
        onSaved();
        setMinutes(30);
        setFocus("");
        setNotes("");
    }

    return (
        <section style={{ padding: "12px 0" }}>
            <h3>Log a Practice Session</h3>
            <form
                onSubmit={submit}
                style={{ display: "grid", gap: 8, maxWidth: 520 }}
            >
                <select
                    value={pieceId}
                    onChange={(e) => setPieceId(Number(e.target.value) || "")}
                    required
                >
                    <option value="">Select a piece…</option>
                    {pieces.map((p) => (
                        <option key={p.id} value={p.id}>
                            {p.title}
                            {p.composer ? ` — ${p.composer}` : ""}
                        </option>
                    ))}
                </select>

                <input
                    type="date"
                    value={practiceDate}
                    onChange={(e) => setPracticeDate(e.target.value)}
                    required
                />
                <input
                    type="number"
                    min={1}
                    max={600}
                    value={minutes}
                    onChange={(e) => setMinutes(Number(e.target.value))}
                    required
                    placeholder="Minutes"
                />
                <input
                    value={focus}
                    onChange={(e) => setFocus(e.target.value)}
                    placeholder="Focus (e.g. technique)"
                />
                <input
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="Notes"
                />

                <button type="submit">Log Session</button>
            </form>
        </section>
    );
}
