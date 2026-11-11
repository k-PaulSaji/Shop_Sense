import re


class HybridSearch:
    def __init__(self, catalog, semantic_index, documents):
        self.catalog = catalog
        self.index = semantic_index
        self.documents = documents

    @staticmethod
    def parse_constraints(query):
        q = query.lower()

        def num(pattern, cast=float):
            match = re.search(pattern, query, re.I)
            return cast(match.group(1).replace(",", "")) if match else None

        return {
            "budget": num(r"(?:under|below|less than|maximum|max(?:imum)?(?: budget)?(?: of)?|up to|upto)\s*(?:inr|₹|rs\.?)?\s*([\d,]+)", int),
            "ram": num(r"(?:at least|min(?:imum)?|with)?\s*(\d+)\s*gb\s*ram", int),
            "size": num(r"(\d+(?:\.\d+)?)\s*[- ]?inch", float),
            "category": next((c for c in ("laptop", "monitor", "headset", "keyboard") if c in q), None),
            "in_stock": bool(re.search(r"\b(in[- ]stock|available|buy now|available now|can i buy|can i order|is .* in stock|is .* available)\b", q)),
        }

    def filter_products(self, query):
        constraints = self.parse_constraints(query)
        products = self.catalog.copy()
        if constraints["category"]:
            products = products[products.category.str.lower() == constraints["category"]]
        if "mechanical" in query.lower():
            products = products[products.apply(
                lambda row: "mechanical" in " ".join(map(str, (row.spec_1, row.spec_2, row.description))).lower(), axis=1
            )]
        if constraints["budget"] is not None:
            products = products[products.price_inr <= constraints["budget"]]
        if constraints["in_stock"]:
            products = products[products.in_stock == 1]
        if constraints["ram"] is not None:
            def ram_ok(row):
                match = re.search(r"(\d+)\s*gb\s*ram", " ".join(map(str, (row.spec_1, row.spec_2, row.description))), re.I)
                return bool(match and int(match.group(1)) >= constraints["ram"])
            products = products[products.apply(ram_ok, axis=1)]
        if constraints["size"] is not None:
            def size_ok(row):
                match = re.search(r"(\d+(?:\.\d+)?)\s*[- ]?inch", " ".join(map(str, (row.spec_1, row.spec_2, row.description))), re.I)
                return bool(match and float(match.group(1)) == constraints["size"])
            products = products[products.apply(size_ok, axis=1)]
        return products, constraints

    def retrieve(self, query, k=8):
        return [(self.documents[index], score) for index, score in self.index.search(query, k)]
