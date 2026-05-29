import csv
import os

# 🛠️ 디버그 옵션: True이면 각 세트별로 딱 1개씩만 만들고 종료, False이면 전체 생성
DEBUG_ONE_FILE = False

print("🧱 멀티 daily_index_X.txt 기반으로 RSS 피드 일괄 생성 시작...")

# 1. dictionary_filtered.csv 파일을 읽어서 메모리에 저장 (공통 데이터)
kanji_db = {}
with open("dictionary_filtered.csv", mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)  # 헤더 스킵
    for row in reader:
        if not row:
            continue
        idx_num = row[0].strip()
        kanji_db[idx_num] = row

# 처리할 학습량 기준 목록
split_counts = [1, 4, 6, 12, 24]

# 2. 각 학습량 버전별로 순회하며 폴더 및 피드 생성
for count in split_counts:
    index_filename = f"daily_index_{count}.txt"
    output_dir = f"../feeds{count}"
    
    # 해당 버전의 폴더 생성 (예: ../feeds1, ../feeds24)
    os.makedirs(output_dir, exist_ok=True)
    
    # 인덱스 파일이 존재하는지 검증 후 읽기
    if not os.path.exists(index_filename):
        print(f"⚠️ {index_filename} 파일이 존재하지 않아 건너뜁니다.")
        continue
        
    with open(index_filename, mode="r", encoding="utf-8") as f:
        days_lines = [line.strip() for line in f if line.strip()]
        
    print(f"📂 {index_filename} 분석 중... (총 {len(days_lines)}일 분량 target -> {output_dir})")

    # 3. 각 파일 내부의 일수(Line)만큼 루프 돌기
    for i, line in enumerate(days_lines):
        day_num = i + 1
        filename = f"{output_dir}/day{day_num:04d}.xml"

        today_indices = [idx.strip() for idx in line.split(",") if idx.strip()]

        # 4. 순수 HTML 태그 뼈대 조립하기
        html_content = ""
        for idx in today_indices:
            if idx in kanji_db:
                _, hanji, level, buseu, eum, hun, ja_on, ja_kun = kanji_db[idx]

                # 한자 하나당 h3와 ul-li 세트로 조립
                html_content += f"          <h3>{hanji}</h3>\n"
                html_content += "          <ul>\n"
                html_content += f"            <li>{level}급 (부수:{buseu})</li>\n"
                html_content += f"            <li>음: {eum} - {ja_on}</li>\n"
                html_content += f"            <li>훈: {hun} - {ja_kun}</li>\n"
                html_content += "          </ul>\n"
                html_content += "          <br/>\n"

        # 5. RSS XML 템플릿에 최종 HTML 박아넣기 (타이틀 글자수 동적 반영)
        rss_template = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>하루 {count}자 일본어 상용한자</title>
    <link>{{{{LINK}}}}</link>
    <description></description>
    <language>ko</language>

    <item>
      <title>오늘의 일본어 상용한자 {count}자</title>
      <link>{{{{LINK}}}}/rss.xml</link>
      <description>
        <![CDATA[
{html_content}        ]]>
      </description>
      <pubDate>{{{{DATE}}}}</pubDate>
      <guid>{{{{LINK}}}}/rss.xml?date={{{{GUID_DATE}}}}</guid>
    </item>
  </channel>
</rss>"""

        # 파일 저장
        with open(filename, mode="w", encoding="utf-8") as out_f:
            out_f.write(rss_template.strip())

        if DEBUG_ONE_FILE:
            print(f"🛑 디버그 모드 작동: {filename} 1개만 뽑고 다음 세트로 넘어갑니다.")
            break

    print(f"✅ 폴더 생성 및 매핑 완료: {output_dir} ({len(days_lines)}개 파일)")

print("-" * 50)
print("🎉 모든 학습량별 RSS 피드 세트 생성이 완벽히 완료되었습니다!")
print("-" * 50)
