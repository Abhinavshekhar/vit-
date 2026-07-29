const cards = [
  ["Now", "Start the highest-risk assignment slice before class."],
  ["Attendance", "Physics is near the threshold. Attend unless OD is approved."],
  ["Deadlines", "Split every deliverable so review happens before the due date."],
  ["Events", "Attend only when networking and skill value beat deadline risk."],
];

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 p-8 text-white">
      <section className="mx-auto max-w-7xl">
        <p className="text-sm uppercase tracking-[0.4em] text-cyan-300">AstraOS</p>
        <h1 className="mt-4 text-5xl font-semibold">Your AI Student Operating System</h1>
        <p className="mt-4 max-w-3xl text-slate-300">
          A production-grade academic command center that understands deadlines, attendance,
          events, energy, and calendar constraints to answer what you should do right now.
        </p>
        <div className="mt-10 grid gap-4 md:grid-cols-4">
          {cards.map(([title, body]) => (
            <article key={title} className="rounded-3xl border border-white/10 bg-white/10 p-6 shadow-2xl backdrop-blur">
              <h2 className="text-xl font-semibold text-cyan-100">{title}</h2>
              <p className="mt-3 text-sm leading-6 text-slate-300">{body}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
