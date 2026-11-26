# Review summary (internal, AI-assisted)

This is a public summary of the internal checking of version 0.1.0, without scores. It is not peer review,
independent reproduction or formal verification. No human referee has assessed the paper.

## What was done (24-25 November 2026)

1. **A five-role Claude review panel** (editor, methodology, domain, perspective, devil's advocate), run as two
   combined review agents, on the source draft. Load-bearing sources were read: Yu (arXiv:2504.02593v2), Fang and
   Huang (arXiv:2610.40486v1), De–Diakonikolas–Servedio, Eskenazis–Nayar–Tkocz, Fang–Wang, Melbourne–Roberto,
   Hollom–Portier, Kontorovich (arXiv:2409.10368v2) and the MathOverflow thread; Haagerup (1981) and Szarek (1976)
   were read from scans and are cited directly.
2. **A full proof audit by the lead** (every theorem re-derived; no error found) and a clean replay of the scripts.
3. **One revision round with extensions**: a context-first introduction and new section order; the unconditional
   results separated from those that use Yu's preprint; the improved total-variation tensorization constant
   (Corollary 4.5); the sharp truncated mean (Corollary 4.3); explicit Hilbert-space stability constants (Remark
   5.2); the necessity half of the threshold interval (Proposition 3.3) with Conjecture 10.1 and numerical evidence;
   the scope of the transfer theorem (Remark 8.3); scripts rewritten without `assert`, plus check_extensions.py.
4. **Verification**: a re-review of everything that changed and a proof audit of the new and rewritten proofs, with an
   independent rerun of check_extensions.py (identical output). The audit found no error in any proof. Four textual
   items were fixed before release (a sentence on which results depend on Yu's preprint, an illustrative example, a
   restated external constant and a symbol clash), together with the minor items.

No Astra/Codex second-model review took place in this batch.

## Main objections and how they were handled

| Objection | Disposition |
|---|---|
| Hard to read; results not separated by dependence | New introduction with a numbered list of results, each marked unconditional or "uses Yu"; notation section; every section opens with its purpose |
| Dependence on an unrefereed preprint | Exact statement of Yu's Theorem 5 as used; conditional results labelled in the abstract, introduction and statements |
| Missing classical references (Ahlswede–Katona, Althöfer–Sillke, Haagerup, Szarek) | Added and cited for what the sources state |
| Proof details (residual margins, explicit constants, nonattainment argument) | Margins printed and checked by script; constants made explicit; argument expanded |
| Scripts relied on `assert` | Explicit checks that exit 1 under `-O`; negative control |
| Wider stop-loss and anti-concentration literature not discussed | Acknowledged limitation; the paper does not rely on it |

## Limits of this checking

No human specialist or editorial review; no independent reproduction by an unaffiliated party; no proof-assistant
formalisation; literature search of limited scope. The scripts check spot cases, the four-dimensional cube and
numerical constants; the general theorems rest on the written proofs.
