import json

from prompting import *
# need to import LLM APIs to get responses for evaluation

# Note: need to calc raw metrics for the model responses (TP, FP, TN, FN) to be able to calculate the evaluation metrics (accuracy, precision, recall, F1 score) for each prompting technique and each model response for comparison
# will prob use an array or smthn for these values mapping the log seq and tag to the model resp along with whether it got TP, FP, TN, FN

# so what im thinking is for each prompting technique
# > load prompt template and associated few-shot examples if applicable
# > load eval dataset
# > create global counters for TP, FP, TN, FN for each LLM to be able to calculate metrics at the end
# > loop through each log sequence in the eval dataset and associated tag (anomalous or normal)
# > prompt the LLM by calling the associated function on each
# > LLM returns the result
# > compare the result of the LLM func to the actual result from the prompting data 
# > if LLM correctly identifies anomalous event, increment TP counter, if it incorrectly identifies anomalous event, increment FP counter, if it correctly identifies normal event, increment TN counter, if it incorrectly identifies normal event, increment FN counter
# > eval metrics function to handle calculating accuracy, precision, recall, F1 score for each LLM based on the TP, FP, TN, FN counters and return results

def load_dataset():
    eval_data_path = os.path.dirname(os.getcwd()) + "/prompting_data/eval_dataset.json"
    with open(eval_data_path, "r") as f:
        eval_dataset = json.load(f)
    return eval_dataset

def eval_gpt(dataset, prompt_template):
    # print("Evaluating GPT with dataset and prompt template...")
    fp, tp, fn, tn = 0, 0, 0, 0
    for data in dataset:
        log_seq = data["log_seq"]
        tag = data["tag"]
        gpt_response = prompt_gpt(log_seq, prompt_template)
        if gpt_response.upper() == "ANOMALOUS":
            if tag.upper() == "ANOMALOUS" or tag.upper() == "MIXED":
                tp += 1
            else:
                fp += 1
        else:
            if tag.upper() == "ANOMALOUS" or tag.upper() == "MIXED":
                fn += 1
            else:
                tn += 1
    
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}
    

def eval_claude(dataset, prompt_template):
    # print("Evaluating Claude with dataset and prompt template...")
    fp, tp, fn, tn = 0, 0, 0, 0
    for data in dataset:
        log_seq = data["log_seq"]
        tag = data["tag"]
        claude_response = prompt_claude(log_seq, prompt_template)
        if claude_response.upper() == "ANOMALOUS":
            if tag.upper() == "ANOMALOUS" or tag.upper() == "MIXED":
                tp += 1
            else:
                fp += 1
        else:
            if tag.upper() == "ANOMALOUS" or tag.upper() == "MIXED":
                fn += 1
            else:
                tn += 1
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}

def eval_gemini(dataset, prompt_template):
    fp, tp, fn, tn = 0, 0, 0, 0
    for data in dataset:
        log_seq = data["log_seq"]
        tag = data["tag"]
        gemini_response = prompt_gemini(log_seq, prompt_template)
        if gemini_response.upper() == "ANOMALOUS":
            if tag.upper() == "ANOMALOUS" or tag.upper() == "MIXED":
                tp += 1
            else:
                fp += 1
        else:
            if tag.upper() == "ANOMALOUS" or tag.upper() == "MIXED":
                fn += 1
            else:
                tn += 1
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}

def eval_zero_shot():
    print("Evaluating zero-shot prompting technique...")
    dataset = load_dataset()
    zero_shot_prompt_template = load_prompt(os.path.dirname(os.getcwd()) + "/prompts/zero-shot.txt")

    print("Evaluating GPT with zero-shot prompting...")
    gpt_results = eval_gpt(dataset, zero_shot_prompt_template)

    print("Evaluating Claude with zero-shot prompting...")
    claude_results = eval_claude(dataset, zero_shot_prompt_template)

    print("Evaluating Gemini with zero-shot prompting...")
    gemini_results = eval_gemini(dataset, zero_shot_prompt_template)

    zero_shot_results = {
        "gpt": gpt_results,
        "claude": claude_results,
        "gemini": gemini_results
    }
    return zero_shot_results


def eval_few_shot():
    print("Evaluating few-shot prompting technique...")
    dataset = load_dataset()
    few_shot_data = json.load(open(os.path.dirname(os.getcwd()) + "/prompting_data/few_shot_prompting_data.json", "r"))
    few_shot_prompt_template = load_prompt(os.path.dirname(os.getcwd()) + "/prompts/few-shot.txt")
    few_shot_prompt_template = few_shot_prompt_template.format(
        baseline_seq="\n".join(few_shot_data[0]["log_seq"]), anomalous_seq="\n".join(few_shot_data[0]["log_seq"])
    )
    print("Evaluating GPT with few-shot prompting...")
    gpt_results = eval_gpt(dataset, few_shot_prompt_template)
    print("Evaluating Claude with few-shot prompting...")
    claude_results = eval_claude(dataset, few_shot_prompt_template)
    print("Evaluating Gemini with few-shot prompting...")
    gemini_results = eval_gemini(dataset, few_shot_prompt_template)
    few_shot_results = {
        "gpt": gpt_results,
        "claude": claude_results,
        "gemini": gemini_results
    }
    return few_shot_results

def eval_chain_of_thought():
    print("Evaluating chain-of-thought prompting technique...")
    dataset = load_dataset()
    chain_of_thought_prompt_template = load_prompt(os.path.dirname(os.getcwd()) + "/prompts/chain-of-thought.txt")
    print("Evaluating GPT with chain-of-thought prompting...")
    gpt_results = eval_gpt(dataset, chain_of_thought_prompt_template)
    print("Evaluating Claude with chain-of-thought prompting...")
    claude_results = eval_claude(dataset, chain_of_thought_prompt_template)
    print("Evaluating Gemini with chain-of-thought prompting...")
    gemini_results = eval_gemini(dataset, chain_of_thought_prompt_template)
    chain_of_thought_results = {
        "gpt": gpt_results,
        "claude": claude_results,
        "gemini": gemini_results
    }
    return chain_of_thought_results

def eval_metrics(results):
    # calculate accuracy, precision, recall, F1 score for each LLM based on the TP, FP, TN, FN counters and return results
    eval_results = {}
    # print("Calculating evaluation metrics for results: ", results)
    for model, res in results.items():
        tp = res["tp"]
        fp = res["fp"]
        fn = res["fn"]
        tn = res["tn"]
        accuracy = (tp + tn) / (tp + fp + fn + tn) if (tp + fp + fn + tn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        eval_results[model] = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score
        }
    return eval_results

def eval():
    zero_shot_results = eval_zero_shot()
    few_shot_results = eval_few_shot()
    chain_of_thought_results = eval_chain_of_thought()
    
    print("Calculating zero-shot prompting metrics...")
    zero_shot_metrics = eval_metrics(zero_shot_results)

    print("Calculating few-shot prompting metrics...")
    few_shot_metrics = eval_metrics(few_shot_results)

    print("Calculating chain-of-thought prompting metrics...")
    chain_of_thought_metrics = eval_metrics(chain_of_thought_results)

    print("\nEvaluation complete\n\n")

    return {
        "zero_shot": zero_shot_metrics,
        "few_shot": few_shot_metrics,
        "chain_of_thought": chain_of_thought_metrics
    }