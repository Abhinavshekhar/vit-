const plan = [
  ["08:30", "Morning brief", "Review attendance risk and top deadline."],
  ["09:00", "Deep work", "Finish the DSA assignment research slice."],
  ["11:00", "Class", "Attend Physics to protect the 75% threshold."],
  ["14:00", "Review", "Convert Gmail findings into confirmed tasks."],
];

const cards = [
  ["Attendance", "Physics 76%", "Attend today. Safe skips: 0."],
  ["Deadlines", "3 active", "Next review block is before the due date."],
  ["Events", "1 recommended", "AI Hackathon beats travel and OD cost."],
  ["Focus", "92 min", "Best energy window starts at 09:00."],
];

export default function Home() {
  return (
    <main className="min-h-screen overflow-hidden bg-[radial-gradient(circle_at_top_left,#164e63,transparent_30%),#020617] p-6 text-white md:p-10">
      <section className="mx-auto max-w-7xl">
        <nav className="flex items-center justify-between rounded-full border border-white/10 bg-white/10 px-5 py-3 shadow-glow backdrop-blur-xl">
          <span className="text-sm font-semibold uppercase tracking-[0.35em] text-cyan-200">AstraOS</span>
          <span className="text-xs text-slate-300">Sync healthy • Planner ready • AI grounded</span>
        </nav>

        <div className="mt-10 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <section className="rounded-[2rem] border border-white/10 bg-white/10 p-8 shadow-glow backdrop-blur-xl">
            <p className="text-sm uppercase tracking-[0.4em] text-cyan-300">What should I do right now?</p>
            <h1 className="mt-4 max-w-3xl text-5xl font-semibold leading-tight md:text-7xl">
              Start the highest-risk task before class.
            </h1>
            <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-300">
              AstraOS combines deadlines, attendance, calendar conflicts, event value, and energy curves into one deterministic plan that the AI can explain.
            </p>
          </section>

          <aside className="rounded-[2rem] border border-cyan-200/20 bg-cyan-200/10 p-6 backdrop-blur-xl">
            <h2 className="text-2xl font-semibold">Today&apos;s perfect plan</h2>
            <div className="mt-6 space-y-4">
              {plan.map(([time, title, detail]) => (
                <div key={time} className="rounded-2xl border border-white/10 bg-slate-950/50 p-4">
                  <p className="text-xs text-cyan-200">{time}</p>
                  <p className="mt-1 font-semibold">{title}</p>
                  <p className="mt-1 text-sm text-slate-400">{detail}</p>
                </div>
              ))}
            </div>
          </aside>
        </div>

        <div className="mt-6 grid gap-4 md:grid-cols-4">
          {cards.map(([title, value, body]) => (
            <article key={title} className="rounded-3xl border border-white/10 bg-white/10 p-6 shadow-2xl backdrop-blur">
              <h2 className="text-sm uppercase tracking-[0.2em] text-cyan-100">{title}</h2>
              <p className="mt-3 text-2xl font-semibold">{value}</p>
              <p className="mt-3 text-sm leading-6 text-slate-300">{body}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
