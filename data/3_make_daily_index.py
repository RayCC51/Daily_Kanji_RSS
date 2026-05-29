import random

print("🎲 이지/하드 인덱스를 무작위로 섞어 멀티 일일 배정표 생성 중...")

# 1. 원본 텍스트 파일 읽기 (줄바꿈 기준으로 리스트화)
with open("dic_easy.txt", "r", encoding="utf-8") as f:
    easy_pool = [line.strip() for line in f if line.strip()]

with open("dic_hard.txt", "r", encoding="utf-8") as f:
    hard_pool = [line.strip() for line in f if line.strip()]

# 배정할 하루당 한자 수 목록
split_counts = [1, 4, 6, 12, 24]
total_kanji = 2136

# 각 분할 기준별로 파일을 생성하기 위한 반복문
for count in split_counts:
    # 매 파일마다 독립적인 무작위 정렬을 위해 인덱스 생성 및 shuffle
    easy_order = list(range(len(easy_pool)))
    hard_order = list(range(len(hard_pool)))
    random.shuffle(easy_order)
    random.shuffle(hard_order)

    daily_lines = []
    e_ptr = 0
    h_ptr = 0
    
    # 총 일수 계산 (예: 2136 / 24 = 89일)
    total_days = total_kanji // count

    for day in range(total_days):
        today_selection = []

        # ----------------------------------------------------
        # 케이스 A: 하루에 1개씩 학습하는 경우 (이지/하드 교대 배정)
        # ----------------------------------------------------
        if count == 1:
            # 이지 주머니에 알맹이가 남아있을 때
            if e_ptr < len(easy_order):
                # 짝수날(0, 2, 4...)은 이지, 홀수날(1, 3, 5...)은 하드
                if day % 2 == 0:
                    random_idx = easy_order[e_ptr]
                    today_selection.append(easy_pool[random_idx])
                    e_ptr += 1
                else:
                    random_idx = hard_order[h_ptr]
                    today_selection.append(hard_pool[random_idx])
                    h_ptr += 1
            # 이지가 먼저 고갈되었을 때 -> 남은 하드에서만 연속 추출
            else:
                random_idx = hard_order[h_ptr]
                today_selection.append(hard_pool[random_idx])
                h_ptr += 1

        # ----------------------------------------------------
        # 케이스 B: 하루에 4, 6, 12, 24개씩 학습하는 경우 (절반씩 분배)
        # ----------------------------------------------------
        else:
            half = count // 2
            remaining_easy = len(easy_order) - e_ptr
            
            # 1. 이지 주머니에 오늘 필요한 '절반(half)'만큼 충분히 남아있을 때
            if remaining_easy >= half:
                # 이지에서 절반(half) 추출
                for _ in range(half):
                    random_idx = easy_order[e_ptr]
                    today_selection.append(easy_pool[random_idx])
                    e_ptr += 1
                # 하드에서 절반(half) 추출
                for _ in range(half):
                    random_idx = hard_order[h_ptr]
                    today_selection.append(hard_pool[random_idx])
                    h_ptr += 1
                    
            # 2. 이지가 완전히 고갈되었거나, 애매하게 부족하게 남았을 때 (IndexError 방지 안전장치)
            else:
                # 남아있는 이지 영혼까지 끌어모으기 (0개면 자동으로 패스됨)
                for _ in range(remaining_easy):
                    random_idx = easy_order[e_ptr]
                    today_selection.append(easy_pool[random_idx])
                    e_ptr += 1
                
                # 하루 채워야 할 총 개수(count) 중 부족한 만큼 전부 하드에서 보충
                needed_hard = count - remaining_easy
                for _ in range(needed_hard):
                    random_idx = hard_order[h_ptr]
                    today_selection.append(hard_pool[random_idx])
                    h_ptr += 1

        # 쉼표로 구분해서 한 줄의 텍스트로 만들기
        daily_lines.append(", ".join(today_selection))

    # 3. 각 버전에 맞는 파일명으로 저장
    output_filename = f"daily_index_{count}.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(daily_lines) + "\n")

    print(f"✅ {output_filename} 생성 완료! (총 {total_days}일 분량)")

print("-" * 50)
print("🎉 모든 조건별 일일 배정표 파일 생성이 완료되었습니다!")
print("-" * 50)
