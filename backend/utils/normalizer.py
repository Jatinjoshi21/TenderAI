import re


def normalize_turnover(value):
    if value is None:
        return None

    value = value.lower()

    # Remove currency symbols and commas
    value = value.replace("rs.", "").replace(",", "").replace("/-", "").strip()

    # Handle crore
    if "crore" in value or "cr" in value:
        number = re.findall(r"\d+\.?\d*", value)
        if number:
            return float(number[0]) * 10000000

    # Handle lakh
    if "lakh" in value or "lac" in value:
        number = re.findall(r"\d+\.?\d*", value)
        if number:
            return float(number[0]) * 100000

    # Default (plain number)
    number = re.findall(r"\d+", value)
    if number:
        return int("".join(number))

    return None


def normalize_projects(value):
    if value is None:
        return None

    number = re.findall(r"\d+", str(value))
    return int(number[0]) if number else None


def normalize_bidder_data(data):
    if data is None:
        return None

    return {
        "company_name": data.get("company_name"),
        "turnover": normalize_turnover(data.get("turnover")),
        "projects_completed": normalize_projects(data.get("projects_completed")),
        "gst_number": data.get("gst_number"),
        "pan_number": data.get("pan_number"),
    }