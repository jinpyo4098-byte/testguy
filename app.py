import streamlit as st
import streamlit.components.v1 as components

# 1. 스트림릿 고유 기능 사용
st.title("여기는 스트림릿 영역입니다")
st.write("파이썬 코드로 쉽게 글씨를 쓸 수 있어요.")

# 2. 질문자님의 HTML 코드를 스트림릿 내부에 삽입하기
html_code =
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>나의 첫 페이지</title>
    <style>
        h1 { color: #FF4B4B; } /* HTML 방식이라 CSS 스타일링도 가능합니다 */
    </style>
</head>
<body>
    <h1>안녕 (이건 HTML로 그린 글씨입니다)</h1>
</body>
</html>

# HTML 컴포넌트를 통해 화면에 렌더링 (가로 700px, 세로 300px 크기의 상자 안에서 작동)
components.html(html_code, height=300)
