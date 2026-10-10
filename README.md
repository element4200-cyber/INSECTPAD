# INSECTPAD

Public stick-figure insect launchpad with a praying mantis mascot.

Live site: https://insectpad.fun

GitHub: https://github.com/element4200-cyber/INSECTPAD

Visitors choose from 12 insects, draw a PFP, or drop in a PNG/JPG/WebP image, upload it, connect Phantom or Solflare, review their token, and approve a Solana mainnet transaction to launch on pump.fun. There is no site account requirement. A compatible wallet, SOL for the initial buy and fees, and pump.fun availability are required.

## Development

Use Node.js 22 or newer. There are no npm dependencies to install.

```sh
npm run build
npm test
npm run validate
npm run dev
```

Local preview runs at http://127.0.0.1:4173. Its upload storage is an in-memory R2 mock and resets when the server stops.

## Source

- `src/page.html`: page, drawing tools, image selection, wallet and launch interface.
- `src/backend.js`: Worker routes, pump.fun integration, PNG generation and upload validation.
- `vendor/solana-web3-1.98.4.iife.min.js`: pinned browser transaction library from @solana/web3.js.
- `scripts/build-worker.mjs`: embeds these sources into `worker/index.js`.
- `scripts/build.mjs`: creates the Worker deployment artifact in `dist/`.
- `tests/`: backend and custom PFP checks. Tests use mocked upstream services and never launch tokens.

## Hosting and configuration

The current public deployment is hosted by Sites. `.openai/hosting.json` retains the existing Site identity and the R2 binding `BUCKET`; publish through the Sites source/version workflow. GitHub stores the source and does not automatically replace the hosted deployment.

The Worker requires durable R2 storage named `BUCKET` for uploaded PFPs and token metadata. Metadata URLs use a fixed SHA-256 identifier to stay below pump.fun's 200-byte URI limit. Optionally set `SOLANA_RPC_URL` to a dedicated HTTPS Solana mainnet RPC. Confirmation falls back to PublicNode and the Solana public mainnet endpoint when a provider is unavailable.

The top banner displays **CA COMING SOON** until `INSECTPAD_MINT` is configured. After launch, set that runtime variable to the verified mint address. The banner, copy button, pump.fun link and live token data then use that address. Never put a private key, wallet seed or service credentials in this repository.

## Launch behavior

`/api/create` asks the pump.fun `https://fun-block.pump.fun/agents/create-coin` endpoint to construct a transaction using public metadata from this site. The visitor reviews and signs it in their own wallet. INSECTPAD never holds a visitor's wallet key. The browser validates the payer and expected programs before asking the wallet to sign, records the submitted signature, and confirms it through Solana RPC.

The launch gallery contains confirmed receipts from the current browser. Custom PFPs are stored by content hash in R2. Network services can return errors; the interface reports failures and can recover a pending launch receipt.

## Insect tutorial

`assets/insect-tutorial.mp4` is a captioned 26-second walkthrough of creating Leaf Larry, drawing a mantis, selecting the PFP, and reviewing the wallet launch. The example button loads an editable draft; visitors upload it themselves and approve launches in their own wallet. The hero mantis dances, hops and spins, with reduced-motion support.
