"use client";

import { useEffect, useState } from "react";
import { getEntries, MoodEntry } from "@/lib/api";

const emojiScore: Record<string, number> = {
  "😄": 5,
  "😊": 5,
  "🙂": 4,
  "😐": 3,
  "😟": 2,
  "😢": 1,
  "😠": 0
};

const scoreHex = ["#ef4444", "#f97316", "#facc15", "#84cc16", "#22c55e", "#10b981"]; // 0‑5

function scoreToHex(score: number): string {
  if (score < 0) return "#d1d5db";
  if (score >= scoreHex.length) return "#10b981";
  return scoreHex[score];
}

export default function HeatMap() {
  const [entries, setEntries] = useState<MoodEntry[]>([]);

  useEffect(() => {
    async function fetchEntries() {
      try {
        const data = await getEntries();
        setEntries(data);
      } catch (err) {
        console.error(err);
      }
    }
    fetchEntries();
  }, []);

  // generate last 7 dates (Mon‑Sun order, ending today)
  const today = new Date();
  const dates = Array.from({ length: 7 }, (_, i) => {
    const d = new Date();
    d.setDate(today.getDate() - (6 - i));
    return d.toISOString().split("T")[0];
  });

  const entryMap = new Map<string, MoodEntry>();
  entries.forEach((e) => entryMap.set(e.date, e));

  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Weekly Mood Heat Map</h2>
      <div className="grid grid-cols-7 gap-2">
        {dates.map((date) => {
          const entry = entryMap.get(date);
          const score = entry ? emojiScore[entry.emoji] ?? 3 : 0;
          const bgColor = entry ? scoreToHex(score) : "#d1d5db";
          const dayLabel = new Date(date).toLocaleDateString(undefined, { weekday: "short" });
          return (
            <div
              key={date}
              style={{ backgroundColor: bgColor }}
              className="h-20 flex items-center justify-center text-white rounded"
              title={entry ? `${entry.emoji} ${entry.note ?? ""}` : "No entry"}
            >
              <span className="text-sm">{dayLabel}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
