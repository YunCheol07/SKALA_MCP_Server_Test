#!/bin/bash

echo "Agent Builder MCP 서버 설정 시작..."

# 1. 가상 환경 생성
echo "가상 환경 생성 중..."
python -m venv venv
source venv/bin/activate

# 2. 의존성 설치
echo "의존성 설치 중..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. 폴더 생성
echo "필수 폴더 생성 중..."
mkdir -p logs

# 4. 환경 변수 설정
echo "환경 변수 설정 중..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env 파일이 생성되었습니다. 필요한 API 키를 입력해주세요."
fi

echo "설정 완료! 서버를 시작하려면 다음 명령을 실행하세요:"
echo "source venv/bin/activate"
echo "python src/server.py"
