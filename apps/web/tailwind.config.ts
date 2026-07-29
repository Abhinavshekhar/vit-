import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        astra: {
          cyan: "#67e8f9",
          violet: "#a78bfa",
          navy: "#020617",
        },
      },
      boxShadow: {
        glow: "0 0 80px rgba(103, 232, 249, 0.16)",
      },
    },
  },
  plugins: [],
};

export default config;
