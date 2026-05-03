def evaluate_bidder(bidder, criteria):
    results = {}

    # 🔹 TURNOVER
    turnover = bidder.get("turnover")
    required_turnover = criteria.get("turnover_min")
    turnover_note = criteria.get("turnover_note")


    if required_turnover is None:
        results["turnover"] = {
            "status": "Needs Review",
            "reason": turnover_note or "Turnover requirement unclear",
            "value": turnover,
            "required": "Unclear"
        }

    elif turnover is None:
        results["turnover"] = {
            "status": "Needs Review",
            "reason": "Turnover data missing or criteria unclear",
            "value": turnover,
            "required": required_turnover
        }
    elif turnover >= required_turnover:
        results["turnover"] = {
            "status": "Eligible",
            "reason": f"{turnover} ≥ {required_turnover}",
            "value": turnover,
            "required": required_turnover
        }
    else:
        results["turnover"] = {
            "status": "Not Eligible",
            "reason": f"{turnover} < {required_turnover}",
            "value": turnover,
            "required": required_turnover
        }

    # 🔹 PROJECTS
    projects = bidder.get("projects_completed")
    required_projects = criteria.get("projects_min")


    if required_projects is None:
        results["projects"] = {
            "status": "Needs Review",
            "reason": "Project requirement unclear",
            "value": projects,
            "required": "Unclear"
        }

    elif projects is None:
        results["projects"] = {
            "status": "Needs Review",
            "reason": "Project data missing or unclear",
            "value": projects,
            "required": required_projects
        }
    elif projects >= required_projects:
        results["projects"] = {
            "status": "Eligible",
            "reason": f"{projects} ≥ {required_projects}",
            "value": projects,
            "required": required_projects
        }
    else:
        results["projects"] = {
            "status": "Not Eligible",
            "reason": f"{projects} < {required_projects}",
            "value": projects,
            "required": required_projects
        }

    # 🔹 GST
    gst = bidder.get("gst_number")
    if criteria.get("gst_required"):
        results["gst"] = {
            "status": "Eligible" if gst else "Not Eligible",
            "reason": "GST present" if gst else "GST missing",
            "value": gst,
            "required": "Required"
        }

    # 🔹 PAN
    pan = bidder.get("pan_number")
    if criteria.get("pan_required"):
        results["pan"] = {
            "status": "Eligible" if pan else "Not Eligible",
            "reason": "PAN present" if pan else "PAN missing",
            "value": pan,
            "required": "Required"
        }

    return results

def final_decision(results):
    statuses = [v["status"] for v in results.values()]

    if "Not Eligible" in statuses:
        return "Not Eligible"

    if "Needs Review" in statuses:
        return "Needs Review"

    return "Eligible"