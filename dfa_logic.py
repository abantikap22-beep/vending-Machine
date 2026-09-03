items = {
    "Muffin": 20,
    "Chocolate": 30,
    "Milkshake": 40
}

VALID_NOTES = {2, 5, 10, 20, 50, 100}
MAX_TOTAL = 100


def process_note(item, current_total, note):
    if item not in items:
        return {
            "status": "REJECTED",
            "dfa_state": "q_reject",
            "message": "Invalid item selected."
        }

    if note not in VALID_NOTES:
        return {
            "status": "REJECTED",
            "dfa_state": "q_reject",
            "message": f"{note} Tk note is invalid."
        }

    price = items[item]
    next_total = current_total + note

    if next_total > MAX_TOTAL:
        return {
            "status": "REJECTED",
            "dfa_state": "q_reject",
            "message": "Total inserted amount cannot exceed 100 Tk."
        }

    if next_total < price:
        return {
            "status": "WAITING",
            "dfa_state": f"q{next_total}",
            "total": next_total,
            "remaining": price - next_total,
            "message": f"Need {price - next_total} Tk more."
        }

    if next_total == price:
        return {
            "status": "ACCEPTED",
            "dfa_state": "q_accept",
            "total": next_total,
            "message": f"Dispensing {item}. Exact payment received."
        }

    return {
        "status": "ACCEPTED",
        "dfa_state": "q_change",
        "total": next_total,
        "change": next_total - price,
        "message": f"Dispensing {item}. Returning Change: {next_total - price} Tk."
    }