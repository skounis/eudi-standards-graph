# EUDI Standards Graph

Interactive graph of how the STS Roadmap (org project 29), the CIR Registry (57) and the Errata Registry (67) link to each other. Built from the public issues in `eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications`.

The page in `site/` has three views:

- **Network map** (`#network`): the whole landscape. CIRs are squares, errata are diamonds.
- **CIR coverage matrix** (`#matrix`): standards × CIRs, with standards that have errata marked.
- **Focus navigator** (`#focus-<issue>`): one item and its neighbours, with a link for each item.

## Refresh the data

Needs `gh` (signed in) and Python 3.

    make start      # serve the page on http://localhost:8000 and open it
    make refresh    # fetch issues, rebuild site/graph.json

Without make: `bash scripts/refresh.sh`, then `python3 -m http.server -d site 8000`.

## How links are inferred

- Scope: issues labelled `wontfix` and feedback issues on specifications ("[TSx] …" or "TSx: …" titles, or issues with no `sts:` label and no standards-body prefix) are left out. `Withdrawn` entries are kept and marked.
- Registry: `CIR` label and a "CIR (EU) …" title = CIR Registry; an "Errata:" title = Errata Registry; everything else = STS Roadmap.
- A `CIR (EU) yyyy/n` label on a standard = the CIR cites it (arrow from CIR to standard).
- Issue links in bodies: erratum → standard = corrects; CIR → CIR = amends; anything else = references. Arrows point from the issue that holds the link.

Project fields (Status, Target Quarter, Responsible body) are not included yet; they need the Projects GraphQL API.
