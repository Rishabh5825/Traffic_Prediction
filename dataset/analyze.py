import csv
from collections import Counter

# Analyze train.csv
with open('train.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"=== TRAIN.CSV ===")
print(f"Total rows: {len(rows)}")
print(f"Columns: {list(rows[0].keys())}")
print()

for col in rows[0].keys():
    values = [r[col] for r in rows]
    missing = sum(1 for v in values if v == '' or v is None)
    unique = len(set(values))
    non_empty = [v for v in values if v != '' and v is not None]
    print(f"\n--- {col} ---")
    print(f"  Unique: {unique}, Missing: {missing} ({missing/len(rows)*100:.1f}%)")
    
    # For categorical columns, show value counts
    if unique <= 20:
        counts = Counter(values)
        for val, cnt in counts.most_common():
            print(f"    '{val}': {cnt}")
    else:
        # Show range for numeric-looking columns
        try:
            nums = [float(v) for v in non_empty]
            print(f"  Min: {min(nums):.4f}, Max: {max(nums):.4f}, Mean: {sum(nums)/len(nums):.4f}")
        except:
            print(f"  Sample values: {list(set(non_empty))[:10]}")

# Analyze test.csv
with open('test.csv', 'r') as f:
    reader = csv.DictReader(f)
    test_rows = list(reader)

print(f"\n\n=== TEST.CSV ===")
print(f"Total rows: {len(test_rows)}")
print(f"Columns: {list(test_rows[0].keys())}")

# Check unique days and timestamps
train_days = sorted(set(int(r['day']) for r in rows))
test_days = sorted(set(int(r['day']) for r in test_rows))
train_ts = sorted(set(r['timestamp'] for r in rows))
test_ts = sorted(set(r['timestamp'] for r in test_rows))
train_geo = sorted(set(r['geohash'] for r in rows))
test_geo = sorted(set(r['geohash'] for r in test_rows))

print(f"\nTrain days: {train_days[:5]}...{train_days[-5:]} (count: {len(train_days)})")
print(f"Test days: {test_days} (count: {len(test_days)})")
print(f"Train timestamps: {train_ts[:5]}...{train_ts[-5:]} (count: {len(train_ts)})")
print(f"Test timestamps: {test_ts[:5]}...{test_ts[-5:]} (count: {len(test_ts)})")
print(f"Train geohashes: {len(train_geo)} unique")
print(f"Test geohashes: {len(test_geo)} unique")
print(f"Geohash overlap: {len(set(train_geo) & set(test_geo))}")
