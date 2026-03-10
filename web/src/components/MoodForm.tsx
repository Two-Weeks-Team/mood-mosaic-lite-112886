"use client";

import { useState } from "react";
import { createEntry } from "@/lib/api";

const emojis = ["😊", "😄", "🙂", "😐", "😟", "😢", "😠"];

export default function MoodForm() {
  const [emoji, setEmoji] = useState(emojis[0]);
  const [note, setNote] = useState("");
  const [status, setStatus] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("Submitting...");
    try {
      const today = new Date().toISOString().split("T")[0];
      await createEntry({ date: today, emoji, note });
      setStatus("Entry saved!");
      setNote("");
    } catch (err: any) {
      setStatus(`Error: ${err.message}`);
    }
    setTimeout(() => setStatus(""), 3000);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col space-y-4 p-4 border rounded bg-white shadow"
    >
      <label className="font-medium">How are you today?</label>
      <select
        value={emoji}
        onChange={(e) => setEmoji(e.target.value)}
        className="p-2 border rounded"
      >
        {emojis.map((e) => (
          <option key={e} value={e}>
            {e}
          </option>
        ))}
      </select>
      <textarea
        placeholder="Optional note (max 255 chars)"
        value={note}
        onChange={(e) => setNote(e.target.value.slice(0, 255))}
        className="p-2 border rounded h-20"
      />
      <button
        type="submit"
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Save Mood
      </button>
      {status && <p className="text-sm">{status}</p>}
    </form>
  );
}
