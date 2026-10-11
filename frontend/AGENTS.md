<!-- LOVABLE:BEGIN -->
> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.
<!-- LOVABLE:END -->

## Application architecture
- Keep TanStack Start's file-based routes and shared root AppShell; this preserves the platform's SSR and routing bootstrap.
- Keep all browser FastAPI requests and endpoint adapters under src/services; this isolates presentation from an adjustable external Python contract.
- Never add a server proxy or inference implementation for this frontend; the user's existing external Python pipeline owns inference and PDF generation.
- Validate API predictions before rendering and show missing numeric outputs as unavailable; this prevents fabricated or corrupted scientific results.
- Use React Query for optional read endpoints and explicit button-triggered multipart prediction submission; uploads must not trigger inference.
- Keep visual roles in src/styles.css semantic tokens and feature components modular; this maintains a coherent hybrid research workspace.
- Prebundle animation, upload, chart, and Radix dependencies through Vite optimizeDeps.include; this avoids late route discovery mixing React cache generations during preview navigation.
