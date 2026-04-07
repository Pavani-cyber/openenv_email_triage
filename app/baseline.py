import json

def baseline_agent(email):
    subj = email["subject"].lower()
    if "urgent" in subj or "asap" in subj:
        return "urgent"
    elif email["sender_domain"] in ["spam.com","junkmail.org"]:
        return "spam"
    elif "follow up" in subj:
        return "followup"
    else:
        return "informational"

if __name__ == "__main__":
    with open("data/sample_emails.json") as f:
        emails = json.load(f)
    results = []
    for e in emails:
        pred = baseline_agent(e)
        results.append({"pred": pred, "true": e["label"]})
    print("Baseline scores:")
    print("Easy:", sum(1 for r in results if r["pred"]==r["true"])/len(results))
