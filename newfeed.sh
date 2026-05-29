#!/bin/sh

DOMAIN_LINK="http://localhost:8080"
# DOMAIN_LINK="https://yourusername.github.io/kanji"
STATUS_FILE="./current_day.txt"
WEB_DIR="./web"

# 배시 배열 대신 모든 쉘에서 호환되는 공백 구분 문자열 사용
SPLIT_COUNTS="1 4 6 12 24"

# 현재 날짜 (RFC 2822 형식)
PUB_DATE=$(date -R)

# 1. 상태 저장 파일이 없거나 비어있다면 기본값 0001로 초기화
if [ ! -f "$STATUS_FILE" ] || [ ! -s "$STATUS_FILE" ]; then
    > "$STATUS_FILE"
    for count in $SPLIT_COUNTS; do
        echo "${count}=0001" >> "$STATUS_FILE"
    done
fi

# 임시 파일 생성 (mktemp가 없는 환경을 위해 일반 파일명 사용 후 삭제)
TMP_STATUS_FILE="./current_day.tmp"
> "$TMP_STATUS_FILE"

# 2. 5개 학습량 세트를 순회하면서 처리
for count in $SPLIT_COUNTS; do
    # current_day.txt에서 해당 count의 현재 일수를 추출 (없으면 0001 기본값)
    CURRENT_NUM=$(grep "^${count}=" "$STATUS_FILE" | cut -d'=' -f2)
    if [ -z "$CURRENT_NUM" ]; then
        CURRENT_NUM="0001"
    fi

    # 3. 다음 날짜 계산 (앞의 0들을 제거해서 8진수 에러 방지 후 연산)
    CLEAN_NUM=$(echo "$CURRENT_NUM" | sed 's/^0*//')
    if [ -z "$CLEAN_NUM" ]; then
        CLEAN_NUM=0
    fi
    
    # 현재 파일 매핑을 위해 패딩 처리
    DAY_STR=$(printf "%04d" $CLEAN_NUM)
    SOURCE_FILE="./feeds${count}/day${DAY_STR}.xml"
    TARGET_FILE="${WEB_DIR}/rss${count}.xml"

    # 4. 만약 현재 날짜 파일이 없다면 (코스가 끝나 고갈되었다면) 1일 차로 로테이션
    if [ ! -f "$SOURCE_FILE" ]; then
        CLEAN_NUM=1
        DAY_STR="0001"
        SOURCE_FILE="./feeds${count}/day0001.xml"
    fi

    # 5. 파일 복사 및 변수 치환 (LINK, DATE)
    cp "$SOURCE_FILE" "$TARGET_FILE"
    
    sed -i "s|{{LINK}}|$DOMAIN_LINK|g" "$TARGET_FILE"
    sed -i "s|{{DATE}}|$PUB_DATE|g" "$TARGET_FILE"

    # 6. 다음 실행을 위해 일수 +1 증가시켜 저장 준비
    NEXT_NUM=$((CLEAN_NUM + 1))
    NEXT_DAY_STR=$(printf "%04d" $NEXT_NUM)

    # 만약 다음 날짜 파일도 없다면 미리 0001로 세팅해서 다음 실행 때 바로 1일차가 되도록 처리
    NEXT_SOURCE_FILE="./feeds${count}/day${NEXT_DAY_STR}.xml"
    if [ ! -f "$NEXT_SOURCE_FILE" ]; then
        NEXT_DAY_STR="0001"
    fi

    echo "${count}=${NEXT_DAY_STR}" >> "$TMP_STATUS_FILE"
    
    echo "🔄 [개수: ${count}] day${DAY_STR}.xml ➡️  ${TARGET_FILE} 업데이트 완료"
done

# 7. 임시 파일을 원본 상태 파일로 덮어쓰기 및 마무리
mv "$TMP_STATUS_FILE" "$STATUS_FILE"

echo "--------------------------------------------------"
echo "🎉 모든 멀티 RSS 피드 변환 및 current_day.txt 갱신 완료!"
echo "--------------------------------------------------"
