#!/usr/bin/env python3
"""Audit every DS page against NORBIELINK-SPEC.md.

Checks only things that are mechanically decidable and actionable. The
green-tinted --gray-* ramp is reported separately, not per page, because it is
a token-level decision that touches the doc-site chrome too.
"""
import re, glob, json, collections, sys

SPEC = {
    # colour -> why it is wrong
    # Corrected 2026-10-14: #EF4444 / #DC2626 / #F59E0B / #73C9B7 / #74C3B7 /
    # #E8622A / #22C55E ARE Norbielink values (status map `eP`, destructive
    # dialogs, form validation, switches, file icons). Only these remain wrong:
    "forbidden_colors": {
        "#1D9E6B": "DS success green — product's positive state is teal #73C9B7",
        "#E6A817": "DS warning amber — product uses #F59E0B",
        "#C0392B": "DS error red — product uses #EF4444",
        "#2980B9": "DS info blue — product has no info state",
        "#B87A00": "DS warning text — product uses #F59E0B",
        "#10B981": "Tailwind green — product's positive state is teal #73C9B7",
        "#059669": "Tailwind green — product's positive state is teal #73C9B7",
        "#047857": "Tailwind green — product's positive state is teal #73C9B7",
        "#4ECDC4": "DS teal-400/500 — product uses #73C9B7",
        "#F97316": "only valid as the activity-feed 'note' icon; switches use #E8622A",
        "#3B82F6": "only valid as promo-card tag content, never as a UI colour",
    },
    "allowed_weights": {"300", "400", "500", "600", "700", "normal", "bold", "inherit"},
    "allowed_radius_px": {"0", "4", "6", "8", "9", "10", "12", "16", "100", "999", "9999"},
}

def styling_context(src):
    """Only the text that actually styles something: <style> blocks and
    style="..." attributes. A hex inside <code> is documentation — the
    retired-colour tables on the Color page are not violations."""
    parts = re.findall(r"<style>(.*?)</style>", src, re.S)
    parts += re.findall(r'style="([^"]*)"', src)
    return "\n".join(parts) if (parts or "<" in src) else src


def scan(path):
    raw = open(path, encoding="utf-8").read()
    s = styling_context(raw) if path.endswith(".html") else raw
    out = collections.defaultdict(list)

    for hexv, why in SPEC["forbidden_colors"].items():
        n = len(re.findall(re.escape(hexv), s, re.I))
        if n:
            out["colour"].append((hexv, n, why))

    for m in re.finditer(r"font-weight:\s*([0-9]+|normal|bold|inherit)", s):
        if m.group(1) not in SPEC["allowed_weights"]:
            out["weight"].append((m.group(1), 1, "not in {400,500,600,700}"))

    # Only component-scale radii are governed. Values under 4px are dots,
    # bars and swatch corners; values over 32px are pills. Neither is a
    # component radius decision.
    for m in re.finditer(r"border-radius:\s*([0-9.]+)px", s):
        f = float(m.group(1))
        if not (4 <= f <= 32):
            continue
        raw = m.group(1)
        # only trim trailing zeros on decimals — "10".rstrip("0") is "1"
        v = raw.rstrip("0").rstrip(".") if "." in raw else raw
        if v not in SPEC["allowed_radius_px"]:
            out["radius"].append((v + "px", 1, "not in {4,6,8,9,10,12,16}"))

    n = len(re.findall(r"Material\+Icons\+Round", raw))
    if n:
        out["icon"].append(("Material Icons Round", n, "filled icon font — product uses outlines"))

    return out

def collapse(items):
    agg = collections.OrderedDict()
    for tok, n, why in items:
        if tok not in agg:
            agg[tok] = [0, why]
        agg[tok][0] += n
    return agg

files = sorted(f for f in glob.glob("ds-*.html"))
totals = collections.Counter()
rows = []
for f in files:
    out = scan(f)
    if not out:
        continue
    n = sum(n for cat in out.values() for _, n, _ in cat)
    totals[f] = n
    rows.append((f, out))

print(f"{len(files)} pages scanned · {len(rows)} with findings · "
      f"{sum(totals.values())} total\n")
for f, out in sorted(rows, key=lambda r: -totals[r[0]]):
    print(f"── {f}  ({totals[f]})")
    for cat in ("colour", "weight", "radius", "icon"):
        if cat not in out:
            continue
        for tok, (n, why) in collapse(out[cat]).items():
            print(f"     {cat:7s} {tok:22s} ×{n:<4d} {why}")
    print()
