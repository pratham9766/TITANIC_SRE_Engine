# React/Vite Frontend Notes

The current hackathon demo is intentionally no-build and runs immediately from `index.html`.

The requested React/Vite/Tailwind stack is scaffolded in:

- `package.json`
- `vite.config.ts`
- `tailwind.config.ts`

Recommended next migration path:

1. Convert `src/data.js` into typed fixtures.
2. Split `src/app.js` into React components:
   - `AppShell`
   - `IncidentHero`
   - `AgentThinkingStream`
   - `InfrastructureGraph`
   - `RiskRadar`
   - `IncidentReplay`
   - `AIChat`
   - `PostmortemGenerator`
3. Replace SVG topology with React Flow.
4. Replace metric sparklines with Recharts.
5. Add Framer Motion variants for page transitions, panel entrance, typing stream, and replay propagation.
6. Add shadcn/ui primitives after dependencies are installed.
