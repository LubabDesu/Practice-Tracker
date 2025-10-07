// src/ui.tsx
import React from "react";

// ui.tsx
const BASE = import.meta.env.VITE_API_BASE_URL || "";
export const Page: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <div
        style={{
            minHeight: "100vh",
            width: "100vh",
            background: "#111",
            color: "#eaeaea",
            fontFamily:
                "Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
            display: "flex",
            justifyContent: "center", // horizontally center
            alignItems: "center", // vertically center
        }}
    >
        <div style={{ width: "100%", maxWidth: 1200, padding: "0 16px" }}>
            {children}
        </div>
    </div>
);

export const Card: React.FC<{
    title?: string;
    children: React.ReactNode;
    right?: React.ReactNode;
}> = ({ title, children, right }) => (
    <section
        style={{
            background: "#1b1b1b",
            border: "1px solid #2a2a2a",
            borderRadius: 12,
            padding: 16,
            boxShadow: "0 4px 20px rgba(0,0,0,.25)",
        }}
    >
        {(title || right) && (
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: 8,
                }}
            >
                {title && <h3 style={{ margin: 0, fontSize: 18 }}>{title}</h3>}
                {right}
            </div>
        )}
        {children}
    </section>
);

export const Grid: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <div
        style={{
            display: "grid",
            gridTemplateColumns: "1fr",
            gap: 16,
        }}
    >
        {children}
        <style>{`
      @media (min-width: 960px) {
        .two-col { display: grid; grid-template-columns: 1.2fr .8fr; gap: 16px; }
      }
    `}</style>
    </div>
);

export const TwoCol: React.FC<{
    left: React.ReactNode;
    right: React.ReactNode;
}> = ({ left, right }) => (
    <div className="two-col">
        {left}
        {right}
    </div>
);

export const Row: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>{children}</div>
);

export const Input = (props: React.InputHTMLAttributes<HTMLInputElement>) => (
    <input
        {...props}
        style={{
            ...props.style,
            padding: "10px 12px",
            borderRadius: 10,
            border: "1px solid #3a3a3a",
            background: "#121212",
            color: "#eaeaea",
            outline: "none",
            minWidth: 0,
        }}
    />
);

export const Button: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement>> = (
    props
) => (
    <button
        {...props}
        style={{
            ...props.style,
            padding: "10px 14px",
            borderRadius: 10,
            border: "1px solid #2e7",
            background: "#2e7",
            color: "#0a0a0a",
            cursor: "pointer",
            fontWeight: 600,
        }}
    />
);

export const LogOutButton = () => (
    <button
        onClick={() => {
            window.location.href = `${BASE}/logout`;
        }}
        style={{
            background: "#333",
            color: "#eee",
            border: "1px solid #555",
            borderRadius: 8,
            padding: "8px 16px",
            cursor: "pointer",
            fontWeight: 500,
            position: "absolute",
            top: 20,
            right: 20,
        }}
    >
        Log Out
    </button>
);
