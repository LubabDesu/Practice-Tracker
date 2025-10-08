import { useEffect, useState } from "react";
import { api } from "./api";
import StatsPanel from "./components/StatsPanel";
import LogSessionForm from "./components/LogSessionForm";
import {
    Page,
    Card,
    Grid,
    TwoCol,
    Row,
    Input,
    Button,
    LogOutButton,
} from "./ui";
import "./App.css";

const BASE = import.meta.env.VITE_API_BASE_URL || "";

type Me = {
    email: string;
    display_name?: string | null;
    total_pieces: number;
    total_sessions: number;
    total_minutes: number;
    current_streak_days: number;
};

type Piece = { id: number; title: string; composer?: string | null };

export default function App() {
    const [me, setMe] = useState<Me | null>(null);
    const [pieces, setPieces] = useState<Piece[]>([]);
    const [title, setTitle] = useState("");
    const [composer, setComposer] = useState("");
    const [status, setStatus] = useState("");
    const [refreshTick, setRefreshTick] = useState(0);
    console.log(BASE);

    function bumpRefresh() {
        load();
        setRefreshTick((t) => t + 1);
    }

    async function load() {
        try {
            const m = await api<Me>("/api/me");
            setMe(m);
            const p = await api<Piece[]>("/api/pieces");
            setPieces(p);
        } catch (e: any) {
            setMe(null);
            setStatus(e.message);
        }
    }

    useEffect(() => {
        load();
    }, []);

    async function addPiece(e: React.FormEvent) {
        e.preventDefault();
        const newPiece = await api<Piece>("/api/pieces", {
            method: "POST",
            body: JSON.stringify({ title, composer: composer || null }),
        });
        setTitle("");
        setComposer("");
        setStatus("Piece added");
        setPieces((prev) => [newPiece, ...prev]);
        await load();
    }

    return (
        <div
            style={{
                minHeight: "100vh",
                background: "#111",
                color: "#eaeaea",
                display: "flex",
                justifyContent: "center", // center horizontally
                alignItems: "center", // or "center" to also center vertically
            }}
        >
            <LogOutButton />
            <div
                style={{ width: "100%", maxWidth: 1100, padding: "24px 16px" }}
            >
                <Page>
                    <header style={{ marginBottom: 16 }}>
                        <h1 style={{ margin: 0, fontSize: 36 }}>
                            Piano Practice Tracker
                        </h1>
                        <p style={{ opacity: 0.7, marginTop: 6 }}>
                            Log. Track. Improve.
                        </p>
                    </header>

                    {!me ? (
                        <Card>
                            <section style={{ textAlign: "center" }}>
                                <p
                                    style={{
                                        fontFamily:
                                            "'Inter', 'Helvetica Neue', sans-serif",
                                        fontSize: "2.2rem",
                                        textAlign: "center",
                                        background:
                                            "linear-gradient(90deg, #c0a3ff, #6fa3ff)",
                                        WebkitBackgroundClip: "text",
                                        WebkitTextFillColor: "transparent",
                                        fontWeight: 700,
                                        marginTop: "1rem",
                                    }}
                                >
                                    {" "}
                                    Join today.
                                </p>
                                <a href={`${BASE}/login?next=/`}>
                                    <Button>Login with Google</Button>
                                </a>
                            </section>
                        </Card>
                    ) : (
                        <Grid>
                            <TwoCol
                                left={
                                    <div style={{ display: "grid", gap: 16 }}>
                                        <Card
                                            title={`Welcome${
                                                me.display_name
                                                    ? `, ${me.display_name}`
                                                    : ""
                                            }`}
                                        >
                                            <p>
                                                <b>{me.email}</b>
                                            </p>
                                        </Card>

                                        <Card
                                            title="Your Stats"
                                            right={
                                                <span style={{ opacity: 0.7 }}>
                                                    🔥 {me.current_streak_days}
                                                    -day streak
                                                </span>
                                            }
                                        >
                                            <StatsPanel refresh={refreshTick} />
                                        </Card>

                                        <Card title="Add a Piece">
                                            <form onSubmit={addPiece}>
                                                <Row>
                                                    <Input
                                                        placeholder="Title"
                                                        value={title}
                                                        onChange={(e) =>
                                                            setTitle(
                                                                e.target.value
                                                            )
                                                        }
                                                        required
                                                    />
                                                    <Input
                                                        placeholder="Composer"
                                                        value={composer}
                                                        onChange={(e) =>
                                                            setComposer(
                                                                e.target.value
                                                            )
                                                        }
                                                    />
                                                    <Button type="submit">
                                                        Add
                                                    </Button>
                                                </Row>
                                            </form>
                                        </Card>

                                        <Card title="Log a Session">
                                            <LogSessionForm
                                                onSaved={bumpRefresh}
                                            />
                                        </Card>
                                    </div>
                                }
                                right={
                                    <div style={{ display: "grid", gap: 16 }}>
                                        <Card title="Your Pieces">
                                            <ul
                                                style={{
                                                    margin: 0,
                                                    paddingLeft: 18,
                                                }}
                                            >
                                                {pieces.map((p) => (
                                                    <li
                                                        key={p.id}
                                                        style={{
                                                            margin: "6px 0",
                                                        }}
                                                    >
                                                        <b>{p.title}</b>
                                                        {p.composer
                                                            ? ` — ${p.composer}`
                                                            : ""}
                                                    </li>
                                                ))}
                                                {pieces.length === 0 && (
                                                    <p style={{ opacity: 0.7 }}>
                                                        No pieces yet.
                                                    </p>
                                                )}
                                            </ul>
                                        </Card>

                                        {/* Optional: recent sessions card if you added SessionsList */}
                                        {/* <Card title="Recent Sessions">
                  <SessionsList refresh={refreshTick}/>
                </Card> */}
                                    </div>
                                }
                            />
                            {status && (
                                <p style={{ color: "seagreen" }}>{status}</p>
                            )}
                        </Grid>
                    )}
                </Page>
            </div>
        </div>
    );
}
