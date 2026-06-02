import csv
import os

CSV_INPUT_PATH = "dictionary_filtered.csv"
CSV_OUTPUT_PATH = "dictionary_with_words.csv"
FREQ_FILE_PATH = "edict_dupefree_freq_distribution"

def is_kanji(ch):
    return '\u4e00' <= ch <= '\u9faf'

kanji_examples = {}
kanji_seen_pairs = {} 

MAX_RANK = 30000    
MAX_EXAMPLES = 5   

print(f"[1/3] 자가복제 1글자 단어를 차단하는 고성능 알고리즘으로 사전 분석을 시작합니다...")

if not os.path.exists(FREQ_FILE_PATH):
    print(f"에러: {FREQ_FILE_PATH} 파일이 없습니다.")
    exit(1)

line_count = 0
valid_word_rank = 0 

with open(FREQ_FILE_PATH, "r", encoding="utf-8") as f:
    for line in f:
        line_count += 1
        line_with = line.strip()
        
        if not line_with or line_with.startswith("#") or "|" not in line_with:
            continue
            
        parts = line_with.split("\t")
        word_info_str = parts[-1]
        word_info = [x.strip() for x in word_info_str.split("|") if x.strip()]
        if not word_info:
            continue
            
        japanese_word = word_info[0]
        
        # 1글자 가나는 무시, 한자 1글자 단어는 우선 허용
        if len(japanese_word) == 1 and not is_kanji(japanese_word[0]):
            continue
            
        valid_word_rank += 1
        if valid_word_rank > MAX_RANK:
            break

        has_reading = False
        reading = ""
        
        if len(word_info) > 1:
            if not word_info[1].startswith("("):
                reading = word_info[1]
                has_reading = True
        
        if has_reading:
            formatted_entry = f"{japanese_word}({reading})"
        else:
            formatted_entry = f"{japanese_word}"
            
        unique_word_key = f"{japanese_word}_{reading if reading else japanese_word}"
            
        for char in japanese_word:
            if is_kanji(char):
                if char not in kanji_examples:
                    kanji_examples[char] = []
                    kanji_seen_pairs[char] = set()
                
                # ⚠️ 핵심 방어막: 한 글자짜리 단어가 자기 자신 한자와 똑같다면 예시에서 제외!
                if len(japanese_word) == 1 and japanese_word == char:
                    continue
                
                if unique_word_key in kanji_seen_pairs[char]:
                    continue
                    
                if len(kanji_examples[char]) < MAX_EXAMPLES:
                    kanji_examples[char].append(formatted_entry)
                    kanji_seen_pairs[char].add(unique_word_key)

print(f"[성공] 자가복제 단어 필터링 및 예시 추출 완료!\n")

# [2단계] CSV 매칭 및 저장 작업
print("[2/3] 기존 한자 목록과 매칭하여 결과 파일을 생성하는 중...")

stats_counts = {i: 0 for i in range(MAX_EXAMPLES + 1)}
total_kanji_count = 0

with open(CSV_INPUT_PATH, "r", encoding="utf-8") as infile, \
     open(CSV_OUTPUT_PATH, "w", encoding="utf-8", newline="") as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    header = next(reader)
    header.append("예시 단어")
    writer.writerow(header)
    
    for row in reader:
        if not row:
            continue
        
        total_kanji_count += 1
        kanji_char = row[1].strip()
        
        examples_list = kanji_examples.get(kanji_char, [])
        count_found = len(examples_list)
        
        stats_counts[count_found] += 1
            
        examples_str = ", ".join(examples_list)
        row.append(examples_str)
        writer.writerow(row)

print("[성공] 파일 쓰기 완료!\n")

print("[3/3] 최종 작업 통계 결과:")
print(f" -> 결과물 저장 완료: {CSV_OUTPUT_PATH}")
for i in range(MAX_EXAMPLES, -1, -1):
    print(f"• 예시 단어 {i}개 매칭된 한자: {stats_counts[i]:>4} 자")
