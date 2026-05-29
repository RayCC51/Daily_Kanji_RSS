import csv

print("⏳ 급수 기준에 따라 인덱스 분리 중...")

csv_file = "dictionary_filtered.csv"
easy_file = "dic_easy.txt"
hard_file = "dic_hard.txt"

easy_indices = []
hard_indices = []

with open(csv_file, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)  # 헤더 스킵 (순번,한자,급수...)
    
    for row in reader:
        if not row:
            continue
            
        index_num = row[0].strip()  # 순번 (예: 1)
        level = float(row[2].strip()) # 급수 (예: 2.5 -> 실수형 변환)
        
        # 10~5급 대역 (숫자가 5 이상인 경우)
        if level >= 5.0:
            easy_indices.append(index_num)
        # 4~2급 대역 (숫자가 5 미만인 경우 - 4, 3, 2.5, 2)
        else:
            hard_indices.append(index_num)

# dic_easy.txt 저장
with open(easy_file, mode="w", encoding="utf-8") as f:
    f.write("\n".join(easy_indices) + "\n")

# dic_hard.txt 저장
with open(hard_file, mode="w", encoding="utf-8") as f:
    f.write("\n".join(hard_indices) + "\n")

print("-" * 50)
print(f"📁 분리 완료!")
print(f"🟢 {easy_file} : {len(easy_indices)} 개 (10~5급 초등 한자 인덱스)")
print(f"🔴 {hard_file} : {len(hard_indices)} 개 (4~2급 중고등 한자 인덱스)")
print("-" * 50)
