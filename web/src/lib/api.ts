export interface MoodEntry {
  id: string;
  date: string;
  emoji: string;
  note?: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "";

export async function createEntry(entry: {
  date: string;
  emoji: string;
  note?: string;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/api/entries`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(entry),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.message || "Failed to create entry");
  }
  return res.json();
}

export async function getEntries(): Promise<MoodEntry[]> {
  const res = await fetch(`${API_BASE}/api/entries`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.message || "Failed to fetch entries");
  }
  const data = await res.json();
  return data.data as MoodEntry[];
}

export async function analyzePatterns(payload: {
  days: number;
  pattern_type: string;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/api/ai/analyze-patterns`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.message || "Pattern analysis failed");
  }
  return res.json();
}

export async function generateInsights(payload: {
  days: number;
  focus: string;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/api/ai/generate-insights`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.message || "Insights generation failed");
  }
  return res.json();
}
