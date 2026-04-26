class AmbiguityRule:
    AMBIGUOUS_WORDS = ["fast", "scalable", "easy", "efficient", "quick"]

    def check(self, text: str):
        issues = []

        for word in self.AMBIGUOUS_WORDS:
            if word in text.lower():
                issues.append({
                    "type": "ambiguity",
                    "message": f"Ambiguous term: '{word}'"
                })

        return issues


class LengthRule:
    def check(self, text: str):
        if len(text.strip()) < 30:
            return [{
                "type": "length",
                "message": "Spec is too short"
            }]
        return []


def run_rules(text: str):
    rules = [
        AmbiguityRule(),
        LengthRule()
    ]

    issues = []

    for rule in rules:
        issues.extend(rule.check(text))

    return issues