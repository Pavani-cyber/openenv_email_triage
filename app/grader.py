def easy_grader(results):
    correct = sum(1 for r in results if r["pred"] == r["true"])
    return correct / len(results)

def medium_grader(results):
    weighted = 0
    for r in results:
        if r["true"] == "urgent":
            weighted += 2 if r["pred"] == "urgent" else 0
        else:
            weighted += 1 if r["pred"] == r["true"] else 0
    return weighted / (len(results)*2)

def hard_grader(results):
    correct = sum(1 for r in results if r["pred"] == r["true"])
    return correct / len(results)
