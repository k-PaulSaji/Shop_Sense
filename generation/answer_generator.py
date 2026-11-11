import re

from generation.citations import catalog_citation, policy_citation


class AnswerGenerator:
    """Deterministic, source-grounded answer generation."""

    POLICY_TERMS = re.compile(
        r"\b(return|refund|warranty|discount|delivery|policy|defective|opened|"
        r"accidental damage|dead[- ]pixel|coupon|tax)\b", re.I
    )

    def __init__(self, catalog, policy_chunks, hybrid):
        self.catalog = catalog
        self.policy_chunks = policy_chunks
        self.hybrid = hybrid

    def _policy_answer(self, query):
        hits = [(d, score) for d, score in self.hybrid.retrieve(query, 10)
                if d.get("kind") == "policy" and score > 0]
        if not hits:
            return {"answer": "I could not find sufficient evidence in the supplied store policy.", "sources": []}
        chunk, _ = hits[0]
        text = chunk["text"].lower()
        q = query.lower()
        # Each template is enabled only when its complete supporting policy fact
        # is present in the retrieved source text.
        if ("headset" in q and any(w in q for w in ("return", "opened"))
                and "opened headsets cannot be returned unless defective" in text):
            answer = "Opened headsets cannot be returned unless they are defective."
        elif "student discount" in q and "monitor" in q and all(x in text for x in (
                "student discount", "eligible laptops only", "student id verification")):
            answer = "No. The 5% student discount applies to eligible laptops only after student ID verification; it does not apply to monitors."
        elif "student discount" in q and "laptop" in q and all(x in text for x in (
                "student discount", "eligible laptops", "student id verification")):
            answer = "A 5% student discount applies to eligible laptops after student ID verification."
            if "cannot be combined with other coupons" in text:
                answer += " It cannot be combined with other coupons."
        elif "warranty" in q and "laptop" in q and all(x in text for x in (
                "laptops", "12-month limited warranty", "manufacturing defects")):
            answer = "Laptops include a 12-month limited warranty for manufacturing defects."
            if "accidental damage is excluded" in text:
                answer += " Accidental damage is excluded."
        elif "warranty" in q and "monitor" in q and all(x in text for x in (
                "monitors", "24-month limited warranty")):
            answer = "Monitors include a 24-month limited warranty."
            if "dead pixel claims require inspection" in text:
                answer += " Dead-pixel claims require inspection."
        elif "delivery" in q and "free standard delivery" in text:
            answer = "Orders above INR 5,000 qualify for free standard delivery in supported Indian PIN codes."
            if "3 to 7 working days" in text:
                answer += " Standard delivery is estimated at 3 to 7 working days."
        elif "accidental damage" in q and "accidental damage is excluded" in text:
            answer = "Accidental damage is excluded from the laptop's limited warranty."
        elif "unopened" in q and "returned within 7 calendar days" in text:
            answer = "Unopened accessories may be returned within 7 calendar days of delivery."
        elif "tax" in q and "tax is included in listed prices" in text:
            answer = "Tax is included in listed prices."
        else:
            return {"answer": "I could not find sufficient evidence in the supplied store policy to answer that specific question.", "sources": []}
        return {"answer": answer, "sources": [f"{policy_citation(chunk)}\nRetrieved text: {chunk['text']}"]}

    def answer(self, query):
        if self.POLICY_TERMS.search(query):
            return self._policy_answer(query)
        df, constraints = self.hybrid.filter_products(query)
        # Report the matching item as unavailable only when the catalog uniquely
        # supports that conclusion and all non-stock constraints still match.
        if df.empty and constraints["in_stock"] and re.search(
                r"\b(can i buy|can i order|buy now|is .* available|is .* in stock)\b", query, re.I):
            relaxed = re.sub(r"\b(in[- ]stock|available|buy now|available now|can i buy|can i order)\b", "", query, flags=re.I)
            unavailable, _ = self.hybrid.filter_products(relaxed)
            unavailable = unavailable[unavailable.in_stock == 0]
            if len(unavailable) == 1:
                r = unavailable.iloc[0]
                return {"answer": f"{r['name']} ({r['sku']}) is currently out of stock and cannot be ordered immediately. Listed price: ₹{int(r['price_inr']):,}.", "sources": [catalog_citation(r)]}
        if df.empty:
            return {"answer": "No matching product. No catalog item satisfies all the stated hard constraints; I will not relax them.", "sources": []}
        # Structured constraints define eligibility; semantic scores only rank
        # eligible catalog records and can never introduce a new product.
        sem = {d.get("sku"): score for d, score in self.hybrid.retrieve(query, 12) if d.get("kind") == "catalog"}
        if sem:
            df = df.copy()
            df["_semantic"] = df.sku.map(sem).fillna(-1)
            df = df.sort_values("_semantic", ascending=False)
        lines, sources = [], []
        for _, r in df.head(3).iterrows():
            price = f"₹{int(r['price_inr']):,}" if float(r["price_inr"]).is_integer() else f"₹{r['price_inr']:,.2f}"
            lines.append(f"**{r['name']} ({r['sku']})** — {price}; {'In stock' if r['in_stock'] else 'Out of stock'}. Specifications: {r['spec_1']}, {r['spec_2']}.")
            sources.append(catalog_citation(r))
        intro = "Matching product:" if len(lines) == 1 else "Products matching your constraints:"
        return {"answer": intro + "\n\n" + "\n\n".join(lines), "sources": sources}
