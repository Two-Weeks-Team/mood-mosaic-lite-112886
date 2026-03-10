"use client";

import MoodForm from "@/components/MoodForm";
import HeatMap from "@/components/HeatMap";

export default function HomePage() {
  return (
    <main className="w-full max-w-2xl space-y-8">
      <h1 className="text-3xl font-bold text-center">{process.env.NEXT_PUBLIC_APP_NAME || "Mood Mosaic Lite"}</h1>
      <MoodForm />
      <HeatMap />
    </main>
  );
}
