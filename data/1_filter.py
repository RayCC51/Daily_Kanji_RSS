import csv

print("⏳ dictionary.csv 파일에서 필요한 컬럼만 추출 중...")

input_file = "dictionary.csv"
output_file = "dictionary_filtered.csv"

# 우리가 남기기로 합의한 8개 정예 컬럼 정의
target_headers = ["순번", "한자", "급수", "부수", "음", "훈", "音", "訓"]

try:
    with open(input_file, mode="r", encoding="utf-8") as infile, \
         open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # 1. 원본 파일의 헤더(첫 줄) 읽기
        original_header = next(reader)
        
        # 원본에서 우리가 필요한 컬럼들의 인덱스 번호(위치) 찾기
        indices = [original_header.index(h) for h in target_headers]
        
        # 2. 새 파일에 우리가 정한 헤더 쓰기
        writer.writerow(target_headers)
        
        # 3. 데이터 줄 돌면서 필요한 데이터만 쏙쏙 골라내서 저장
        row_count = 0
        for row in reader:
            if not row:
                continue
            
            # 각 행에서 타겟 인덱스에 해당하는 값만 추출하고 양쪽 공백 제거
            clean_row = [row[idx].strip() for idx in indices]
            
            # 훈(뜻)이나 일본어 독음 내부에 혹시 있을지 모르는 줄바꿈(\n) 정리
            clean_row[5] = clean_row[5].replace("\n", " ").replace("\r", "") # 훈
            
            writer.writerow(clean_row)
            row_count += 1

    print("-" * 50)
    print(f"🎉 필터링 완료! 불필요한 노이즈가 제거된 '{output_file}'이 생성되었습니다.")
    print(f"📊 총 처리된 한자 수: {row_count} 개")
    print("-" * 50)

except FileNotFoundError:
    print(f"❌ 에러: {input_file} 파일을 찾을 수 없습니다. 경로를 확인해 주세요.")
except ValueError as e:
    print(f"❌ 에러: 원본 CSV에 필요한 컬럼이 누락되었습니다. ({e})")
