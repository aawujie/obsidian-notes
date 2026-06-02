---
title: "You Can Now Build a Hedge Fund from AI Agents"
type: article
created: 2026-06-02
updated: 2026-06-02
sources:
  - "https://x.com/phosphenq/status/2061517261308146058"
tags:
  - ai-agent
  - hedge-fund
  - quant
  - open-source
---

# You Can Now Build a Hedge Fund from AI Agents

**作者:** Phosphen (@phosphenq)
**发布时间:** 2026-06-01T18:36:30.000Z
**互动:** 183 likes | 11 RT | 388 bookmarks

---

> I build quant tooling for a living, and lately every group chat I'm in has sent me the same repo. So I cloned all of it, wired it up, ran it on live SEC data, and pointed it at Polymarket. Here's exactly what's inside, what to install, how to drive it with Claude Code, and where the real edge actually is.

Picture Warren Buffett, Michael Burry and Stan Druckenmiller in one room, fighting over the same stock.

Buffett wants the moat. Burry wants to know what's quietly broken. Druckenmiller is reading the macro and sizing the bet.

Now run that fight on your laptop tonight, for the price of an API call. That's where we are.

Two open-source repos kicked this off, and the star charts tell the story better than I can.

> virattt/ai-hedge-fund ★ 59.6K
14 famous-investor agents, four quant analysts, a risk manager and a portfolio manager / 19 agents in one pipeline.

This is the one with the celebrity names. Fourteen agents, each given one investor's playbook: Buffett hunts moats, Burry hunts what's broken, Druckenmiller reads the macro, Damodaran runs the valuation, Ben Graham checks the margin of safety.

Behind them sit four quant agents (valuation, sentiment, fundamentals, technicals), a risk manager, and a portfolio manager that makes the actual call. Nineteen agents, running in sequence.

Getting it live takes about three commands:

Add --ollama and the whole thing runs on a local model, nothing leaving your machine. There's a backtester next to it, and a web UI in /app if you'd rather click than type.

It's built for learning, not for sending real orders. But as a map of how you wire analysts into reasoners into a decision, it's the best free teacher on GitHub.

> TauricResearch/TradingAgents ★ 81.6K 
the institutional version: desk roles instead of celebrities, with a bull-vs-bear debate at the center.

Same idea, grown up. It drops the famous names for the roles a real desk actually runs: a fundamentals analyst, a sentiment analyst pulling StockTwits and Reddit, a news analyst on the macro, a technical analyst on MACD and RSI.

Then comes the part I care about. Their findings go into a structured debate, a bull researcher and a bear researcher arguing it out, before a trader and a risk layer ever see it.

> Two agents arguing cancels a single model's confident wrong answer in a way one prompt never can.

You control how hard they fight. The whole thing is config:

Setup is a conda env, pip install., an LLM key plus an Alpha Vantage key for prices. StockTwits and Reddit are baked in. Then tradingagents drops you into an interactive CLI.

Here's the thing nobody mentions in the viral threads. Point any of these agents at a ticker with no real data behind it, and it will read whatever's in its training memory and hand you a confident, beautifully-written guess.

> The model was never the moat. The data you wire underneath it is.

So before the agents, you build the part that does the quiet work: a layer that pulls real filings, and never lets the model make a number up.

> dgunning/edgartools ★ 2.3M downloads 
turns every SEC filing into clean Python, and ships an MCP server so Claude reads the real thing.

Every US public company files with the SEC, and the SEC gives all of it away through a free API called EDGAR. edgartools parses those filings (10-Ks, 8-Ks, insider Form 4s, 13F holdings) into clean, typed Python.

No key, no signup, just an email for identity. It got pulled into Anthropic's Claude for Open Source program, and for good reason, which brings me to the part that changes how you use it.

If you want a full cockpit on top of that, OpenBB is the open-source Bloomberg terminal, dozens of data vendors behind one interface, MCP included.

edgartools ships an MCP server. That means you don't import it and write glue code, you hand it to Claude as a tool. Drop this into your Claude Desktop or Claude Code config:

Now you can tell Claude "compare Nvidia and AMD revenue growth over three years," and it pulls the actual filings through thirteen EDGAR tools instead of inventing numbers that merely sound right.

This is also how I built everything you're reading about. I didn't hand-write the plumbing, I drove Claude Code: clone the repo, set up the env, wire the keys, debug the one filing that parses weird. Codex does the same job.

> The new quant skill isn't writing every line. It's directing an agent that writes them, and knowing exactly what to verify.

Real data is half of it. The other half is disciplined math that tells you which filings are even worth opening.

> JerBouma/FinanceToolkit ★ 150+ ratios 
Beneish, Altman, Piotroski, Sloan, all with the formulas written out so you can audit them.

Academics built these scores off decades of real fraud and bankruptcy. Each one flags a different kind of trouble.

Don't reimplement these off a random blog, by the way. Half the M-Score code on GitHub is subtly wrong. Use the maintained library.

So I Ran One on Live Data

The simplest of the four is the accruals ratio, the heaviest single input in Beneish: net income minus operating cash flow, over total assets.

The fastest way to fake a profit is to book income that never showed up as cash. So the higher this runs, the more the earnings are outrunning the money behind them.

I pointed it at sixteen megacaps. Here's the raw output, every number live from EDGAR:

Now Read That Result Like a Quant

Not one name trips the flag. That's the lesson, not a letdown. These are the most picked-over companies on earth, so the screen's job isn't to find fraud in Apple. It's to take a thousand filings and float the few where profit is outrunning cash to the top, so you read those instead of all thousand.

> Nvidia leads at +8.4%. Not because it's cooking books, but because hypergrowth books sales faster than the cash lands. A flag doesn't shout "fraud." It whispers "go look."

Apple sits at +0.1%, its profit and its cash basically the same number.

One honest detail the live run forced on me: Apple and Disney tag operating cash flow under a concept the convenience function missed, so the script had to grab it from the standardized line instead. Every real pipeline has an exotic-filer edge case. The tooling just tells you where it is.

This is the part I'm most interested in, because the discipline transfers cleanly to prediction markets.

On Poly the "10-K" becomes the market's resolution source plus whatever live data settles it. The agents read that instead of a filing, the math becomes "is this implied probability backed by evidence or by narrative," and the edge is, again, the wiring.

It's not theoretical. More than 30% of Polymarket wallets already run agents, and most of the consistently profitable wallets are bots

> Polymarket Toolkit ★ open-source
Brier scoring, audit-grade P/L, address analysis - built by an independent trader using Claude Code and Codex.

That toolkit is the prediction-market version of everything above: polymarket-brier scores how calibrated a trader's predictions actually are, polymarket-pnl reconstructs profit and loss to the cent, polymarket-profile reads any wallet. Same recipe, different ledger. Real data in, disciplined math on top, an agent writing the memo.

If you've read my Poly breakdowns before, this is where the forensic habit and the prediction-market habit finally become the same skill.

Step back and it's four layers. The agents everyone screenshots are the top one. The three underneath are where the work, and the edge, actually live.

And the part that should sting anyone paying $24,000 a year for a terminal: every layer is open source.

The order you assemble it in is the entire game:

Everyone is about to have the same models and the same famous-investor prompts. Pasting a 10-K into a chat box and asking "is this a good company" will feel like research, and produce nothing.

The people three steps ahead wired the model to EDGAR, let the math decide what's worth reading, and spent the model's intelligence on the one thing it's genuinely great at: the language buried on page ninety-four.

So here's the question I keep coming back to. When the models are commodities and the prompts are public, what's actually left to compete on?

The boring part. The wiring.

In the last two breakdowns here we asked whether a strategy is real or just random, and whether a market has memory. Next I'll turn this screen into the full four-score version that runs across a live watchlist and a Polymarket book at the same time. Want it?

> Not financial advice. The persona funds are educational projects. Verify before you commit.

