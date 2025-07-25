import os
import json

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def extract_headings(outline):
    # Returns set of (level, text, page) for comparison
    return set((h["level"], h["text"].strip(), h["page"]) for h in outline.get("outline", []))

def evaluate(pred_dir, gt_dir):
    all_tp, all_fp, all_fn = 0, 0, 0
    for fname in os.listdir(gt_dir):
        if not fname.endswith(".json"):
            continue
        gt_path = os.path.join(gt_dir, fname)
        pred_path = os.path.join(pred_dir, fname)
        if not os.path.exists(pred_path):
            print(f"Missing prediction for {fname}")
            continue
        gt = load_json(gt_path)
        pred = load_json(pred_path)
        gt_headings = extract_headings(gt)
        pred_headings = extract_headings(pred)
        tp = len(gt_headings & pred_headings)
        fp = len(pred_headings - gt_headings)
        fn = len(gt_headings - pred_headings)
        all_tp += tp
        all_fp += fp
        all_fn += fn
        print(f"{fname}: Precision={tp/(tp+fp+1e-9):.2f}, Recall={tp/(tp+fn+1e-9):.2f}")
    precision = all_tp / (all_tp + all_fp + 1e-9)
    recall = all_tp / (all_tp + all_fn + 1e-9)
    f1 = 2 * precision * recall / (precision + recall + 1e-9)
    print(f"\nOverall: Precision={precision:.2f}, Recall={recall:.2f}, F1={f1:.2f}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_dir", required=True, help="Directory with predicted JSONs")
    parser.add_argument("--gt_dir", required=True, help="Directory with ground truth JSONs")
    args = parser.parse_args()
    evaluate(args.pred_dir, args.gt_dir) 