#!/usr/bin/env python3
"""
Compare prediction outputs between two DeepEC runs.
Checks for differences in predictions and numerical accuracy.
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path


def compare_predictions(file1, file2, tolerance=1e-3):
    """Compare two prediction files with numerical tolerance"""
    try:
        df1 = pd.read_csv(file1, sep="\t")
        df2 = pd.read_csv(file2, sep="\t")
    except Exception as e:
        print(f"Error reading files: {e}")
        return False

    if len(df1) != len(df2):
        print(f"Different number of predictions: {len(df1)} vs {len(df2)}")
        return False

    differences = []
    numeric_cols = df1.select_dtypes(include=[np.number]).columns

    for idx in range(len(df1)):
        row_diff = []
        for col in df1.columns:
            val1, val2 = df1.iloc[idx][col], df2.iloc[idx][col]

            if col in numeric_cols:
                if pd.notna(val1) and pd.notna(val2):
                    if abs(val1 - val2) > tolerance:
                        row_diff.append(
                            f"{col}: {val1:.6f} vs {val2:.6f} (diff: {abs(val1-val2):.6e})"
                        )
            else:
                if str(val1) != str(val2):
                    row_diff.append(f"{col}: '{val1}' vs '{val2}'")

        if row_diff:
            differences.append(f"Row {idx}: " + ", ".join(row_diff))

    if differences:
        print(f"Found {len(differences)} differences:")
        for diff in differences[:10]:  # Show first 10
            print(f"  {diff}")
        if len(differences) > 10:
            print(f"  ... and {len(differences) - 10} more")
        return False
    else:
        print("✓ Files match within tolerance")
        return True


def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_outputs.py <output_dir_old> <output_dir_new>")
        sys.exit(1)

    dir_old = Path(sys.argv[1])
    dir_new = Path(sys.argv[2])

    files_to_compare = [
        "log_files/Enzyme_prediction.txt",
        "log_files/4digit_EC_prediction.txt",
        "log_files/3digit_EC_prediction.txt",
        "log_files/Blastp_result.txt",
        "DeepEC_Result.txt",
    ]

    all_match = True
    for file in files_to_compare:
        f1, f2 = dir_old / file, dir_new / file
        if not f1.exists() or not f2.exists():
            print(f"⚠ Skipping {file} (not found in both directories)")
            continue

        print(f"\nComparing {file}...")
        if not compare_predictions(f1, f2):
            all_match = False

    print("\n" + "=" * 60)
    if all_match:
        print("✓ All predictions match!")
    else:
        print("✗ Some predictions differ - review above")

    sys.exit(0 if all_match else 1)


if __name__ == "__main__":
    main()
