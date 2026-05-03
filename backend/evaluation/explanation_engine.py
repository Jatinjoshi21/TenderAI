
from evaluation.evaluator import final_decision


def generate_final_output(bidder_name, results):
    final_status = final_decision(results)

    return {
        "bidder": bidder_name,
        "criteria_results": results,
        "final_status": final_status
    }