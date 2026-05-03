import re


def simplify_criteria(raw_criteria):
    simplified = {}

    # 🔹 Turnover
    turnover = raw_criteria.get("turnover_min")

    if turnover is None:
        simplified["turnover_min"] = None

    elif "%" in turnover:
        # Cannot compute without estimated cost
        simplified["turnover_min"] = None
        simplified["turnover_note"] = "Percentage-based (Needs Review)"

    else:
        # Try extracting number
        nums = re.findall(r"\d+", turnover.replace(",", ""))
        simplified["turnover_min"] = int(nums[0]) if nums else None

    # 🔹 Projects
    projects = raw_criteria.get("projects_min")

    if projects:
        # Extract minimum number mentioned
        nums = re.findall(r"\d+", projects)
        simplified["projects_min"] = int(nums[0]) if nums else None
    else:
        simplified["projects_min"] = None

    # 🔹 GST & PAN
    simplified["gst_required"] = raw_criteria.get("gst_required", True)
    simplified["pan_required"] = raw_criteria.get("pan_required", True)

    return simplified