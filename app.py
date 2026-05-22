import streamlit as st
import streamlit.components.v1 as components

# 스트림릿 페이지 설정
st.set_page_config(page_title="Gravity Arrow", layout="wide")

# 게임 HTML/CSS/JavaScript 코드
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gravity Arrow</title>
    <style>
        /* 우주적인 디자인 컨셉 (Cosmic Theme) */
        body {
            margin: 0;
            padding: 0;
            background: radial-gradient(circle, #1b2735 0%, #090a0f 100%);
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow: hidden;
            user-select: none;
        }

        #game-container {
            position: relative;
            width: 800px;
            margin-top: 10px;
        }

        /* 배경 이미지 교체를 위한 스타일 힌트 */
        #game-canvas {
            border: 2px solid #4a5568;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 150, 255, 0.3);
            background-color: rgba(0, 0, 0, 0.4);
            /* 배경 사진을 추가하려면 아래 주석을 해제하고 경로를 넣으세요 */
            /* background-image: url('YOUR_PLANET_BACKGROUND_URL'); */
            /* background-size: cover; */
            cursor: crosshair;
        }

        .header {
            text-align: center;
            margin-bottom: 5px;
        }

        h1 {
            font-size: 2.5rem;
            margin: 5px 0;
            text-shadow: 0 0 10px #00d2ff;
            font-weight: 800;
            letter-spacing: 2px;
        }

        .ui-panel {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 800px;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 20px;
            border-radius: 8px;
            box-sizing: border-box;
            margin-bottom: 10px;
            backdrop-filter: blur(5px);
        }

        .stats {
            font-size: 1.1rem;
            font-weight: bold;
        }

        .btn {
            background: linear-gradient(135deg, #00d2ff 0%, #0066ff 100%);
            border: none;
            color: white;
            padding: 8px 16px;
            font-size: 1rem;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 15px rgba(0, 102, 255, 0.4);
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 132, 255, 0.6);
        }

        .btn:active {
            transform: translateY(1px);
        }

        /* 행성 선택 스타일 */
        .planet-selector {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .planet-circle {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: bold;
            text-shadow: 1px 1px 2px #000;
        }

        .planet-circle:hover {
            transform: scale(1.1);
        }

        .planet-circle.active {
            border-color: #fff;
            box-shadow: 0 0 15px currentColor;
        }

        /* 각 행성별 임시 구체 디자인 (추후 사진 대체 가능) */
        #planet-earth { background: radial-gradient(circle at 30% 30%, #2b82c9, #053057); color: #00d2ff; }
        #planet-moon { background: radial-gradient(circle at 30% 30%, #ccc, #666); color: #ddd; }
        #planet-mars { background: radial-gradient(circle at 30% 30%, #e03e1d, #5c1303); color: #ff6b6b; }
        #planet-venus { background: radial-gradient(circle at 30% 30%, #e3a857, #6d3e00); color: #ffd166; }
        #planet-europa { background: radial-gradient(circle at 30% 30%, #a5cad6, #3a5d6b); color: #98e1f5; }
    </style>
</head>
<body>

    <div class="header">
        <h1>Gravity Arrow</h1>
        <button class="btn" id="start-btn" onclick="startGame()">Start Game</button>
    </div>

    <div class="ui-panel">
        <div class="stats">
            시간: <span id="time-disp">15</span>s | 
            중력: <span id="gravity-disp">9.8</span> $m/s^2$ | 
            점수: <span id="score-disp">0</span> | 
            최고기록: <span id="high-disp">0</span>
        </div>
        
        <div class="planet-selector">
            <button class="btn" onclick="cyclePlanet()">Change</button>
            <div id="planet-earth" class="planet-circle active" onclick="selectPlanet('earth')">지구</div>
            <div id="planet-moon" class="planet-circle" onclick="selectPlanet('moon')">달</div>
            <div id="planet-mars" class="planet-circle" onclick="selectPlanet('mars')">화성</div>
            <div id="planet-venus" class="planet-circle" onclick="selectPlanet('venus') font-size: 0.65rem;">금성</div>
            <div id="planet-europa" class="planet-circle" onclick="selectPlanet('europa')">유로파</div>
        </div>
    </div>

    <div id="game-container">
        <canvas id="game-canvas" width="800" height="450"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');

        // 행성 데이터 (중력값 m/s^2 공식 반영 및 물리 스케일링)
        const planets = {
            earth: { name: '지구', gravity: 9.8, color: '#2b82c9' },
            moon: { name: '달', gravity: 1.6, color: '#ccc' },
            mars: { name: '화성', gravity: 3.7, color: '#e03e1d' },
            venus: { name: '금성', gravity: 8.9, color: '#e3a857' },
            europa: { name: '유로파', gravity: 1.3, color: '#a5cad6' }
        };
        const planetKeys = ['earth', 'moon', 'mars', 'venus', 'europa'];
        let currentPlanetKey = 'earth';

        // 게임 변수
        let score = 0;
        let highScore = localStorage.getItem('gravity_arrow_high') || 0;
        let timeLeft = 15;
        let gameActive = false;
        let gameInterval;
        let timerInterval;

        // 물리 환경 변수
        let gravityScale = 0.03; // 화면 해상도에 맞춘 중력 스케일 계수
        let currentGravity = planets[currentPlanetKey].gravity * gravityScale;

        // 과녁 변수 (위아래 이동)
        let target = {
            x: 720,
            y: 225,
            radiusD: 50, // 1점
            radiusC: 35, // 2점
            radiusB: 20, // 5점
            radiusA: 8,  // 10점 (작음)
            speed: 1.5,
            dir: 1
        };
        
        // 활 및 화살 변수
        const bowPos = { x: 80, y: 225 };
        let isDragging = false;
        let dragStart = { x: 0, y: 0 };
        let dragEnd = { x: 0, y: 0 };
        
        let activeArrows = [];
        let currentArrow = { isApple: false };
        
        // 애플 화살 관련 팅김 타이머
        let appleTimer = 0;
        let appleTrajectoryVisible = true;

        // 최고 기록 초기 초기화
        document.getElementById('high-disp').innerText = highScore;

        // 행성 선택 함수
        function selectPlanet(key) {
            currentPlanetKey = key;
            planetKeys.forEach(k => {
                document.getElementById(`planet-${k}`).classList.remove('active');
            });
            document.getElementById(`planet-${key}`).classList.add('active');
            
            // 중력 표기 (소수점 1자리)
            document.getElementById('gravity-disp').innerText = planets[key].gravity.toFixed(1);
            currentGravity = planets[key].gravity * gravityScale;
            
            // 행성별 배경 교체용 커스텀 이벤트나 스타일 처리를 여기에 추가할 수 있습니다.
            generateStars(); 
        }

        // Change 버튼 클릭 시 순환
        function cyclePlanet() {
            let idx = planetKeys.indexOf(currentPlanetKey);
            idx = (idx + 1) % planetKeys.length;
            selectPlanet(planetKeys[idx]);
        }

        // 게임 시작
        function startGame() {
            if(gameActive) return;
            score = 0;
            timeLeft = 15;
            gameActive = true;
            activeArrows = [];
            rollNextArrow();

            document.getElementById('score-disp').innerText = score;
            document.getElementById('time-disp').innerText = timeLeft;
            document.getElementById('start-btn').innerText = "게임 진행 중";
            document.getElementById('start-btn').disabled = true;

            // 과녁 방향 전환 타이머 (5초마다)
            let targetDirInterval = setInterval(() => {
                if(!gameActive) clearInterval(targetDirInterval);
                target.dir *= -1;
            }, 5000);

            // 1초 단위 타이머
            timerInterval = setInterval(() => {
                timeLeft--;
                document.getElementById('time-disp').innerText = timeLeft;
                if(timeLeft <= 0) {
                    endGame();
                }
            }, 1000);

            // 루프 시작
            gameInterval = requestAnimationFrame(update);
        }

        // 게임 종료
        function endGame() {
            gameActive = false;
            cancelAnimationFrame(gameInterval);
            clearInterval(timerInterval);
            
            if(score > highScore) {
                highScore = score;
                localStorage.setItem('gravity_arrow_high', highScore);
                document.getElementById('high-disp').innerText = highScore;
                alert(`축하합니다! 최고기록 달성: ${score}점`);
            } else {
                alert(`게임 종료! 최종 점수: ${score}점`);
            }

            document.getElementById('start-btn').innerText = "Start Game";
            document.getElementById('start-btn').disabled = false;
        }

        // 1/20 확률의 사과 화살 결정
        function rollNextArrow() {
            currentArrow = {
                isApple: Math.random() < 0.05 // 20분의 1 확률
            };
            appleTimer = 0;
            appleTrajectoryVisible = true;
        }

        // 마우스 및 드래그 이벤트 처리 (Angry Birds 방식 포물선)
        canvas.addEventListener('mousedown', (e) => {
            if(!gameActive) return;
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            // 활 근처에서 드래그 시작할 수 있도록 세팅
            if(Math.hypot(mouseX - bowPos.x, mouseY - bowPos.y) < 60) {
                isDragging = true;
                dragStart = { x: bowPos.x, y: bowPos.y };
                dragEnd = { x: mouseX, y: mouseY };
            }
        });

        canvas.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            const rect = canvas.getBoundingClientRect();
            dragEnd = { x: e.clientX - rect.left, y: e.clientY - rect.top };
        });

        canvas.addEventListener('mouseup', (e) => {
            if (!isDragging) return;
            isDragging = false;

            // 잡아당긴 벡터 계산 (반대 방향으로 발사)
            const dx = dragStart.x - dragEnd.x;
            const dy = dragStart.y - dragEnd.y;
            
            // 발사 속도 기본 물리 척도 설정 (유저 조건: 기본속도 기반 빠른 연출)
            const speedScale = 0.25; 
            const vx = dx * speedScale;
            const vy = dy * speedScale;

            // 화살이 너무 제자리에 떨어지거나 뒤로 가지 않게 최소 앞방향 추진력 제한
            if(vx > 2) {
                activeArrows.push({
                    x: bowPos.x,
                    y: bowPos.y,
                    vx: vx,
                    vy: vy,
                    isApple: currentArrow.isApple,
                    width: canvas.width / 16, // 크기 조건: 화면의 16분의 1 크기 (약 50px)
                    height: 4,
                    collided: false
                });
                rollNextArrow(); // 즉시 다음 화살 장전 (조건 4-4, 4-5)
            }
        });

        // 배경 별 무작위 생성 효과
        let stars = [];
        function generateStars() {
            stars = [];
            for(let i=0; i<40; i++) {
                stars.push({x: Math.random()*canvas.width, y: Math.random()*canvas.height, r: Math.random()*1.5});
            }
        }
        generateStars();

        // 메인 업데이트 및 그리기 루프
        function update() {
            if(!gameActive) return;

            // 1. 물리 연산 - 과녁 이동
            target.y += target.speed * target.dir;
            if(target.y - target.radiusD < 0 || target.y + target.radiusD > canvas.height) {
                target.dir *= -1; // 캔버스 벽면 충돌 방지 예외처리
            }

            // 애플 화살 전용 타이머 연산 (1초마다 점선 가시성 반전)
            if(currentArrow.isApple) {
                appleTimer++;
                if(appleTimer % 60 === 0) { // 약 1초 (60프레임)
                    appleTrajectoryVisible = !appleTrajectoryVisible;
                }
            }

            // 2. 그리기 작업
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 우주 배경 성단 그리기
            ctx.fillStyle = "rgba(255,255,255,0.3)";
            stars.forEach(s => {
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
                ctx.fill();
            });

            // 과녁 그리기 (A, B, C, D 단계 과녁 고유 색상 및 점수)
            // 외곽부터 그림 (D -> C -> B -> A)
            const targetColor = planets[currentPlanetKey].color;
            
            ctx.fillStyle = "rgba(255,255,255,0.2)";
            ctx.strokeStyle = targetColor;
            ctx.lineWidth = 2;
            
            // D구역 (1점)
            ctx.beginPath(); ctx.arc(target.x, target.y, target.radiusD, 0, Math.PI*2); ctx.fill(); ctx.stroke();
            // C구역 (2점)
            ctx.fillStyle = "rgba(255,255,255,0.15)";
            ctx.beginPath(); ctx.arc(target.x, target.y, target.radiusC, 0, Math.PI*2); ctx.fill(); ctx.stroke();
            // B구역 (5점)
            ctx.fillStyle = "rgba(255,255,255,0.25)";
            ctx.beginPath(); ctx.arc(target.x, target.y, target.radiusB, 0, Math.PI*2); ctx.fill(); ctx.stroke();
            // A구역 (10점 - 작음)
            ctx.fillStyle = "#ff007f";
            ctx.beginPath(); ctx.arc(target.x, target.y, target.radiusA, 0, Math.PI*2); ctx.fill(); ctx.stroke();

            // 활(Bow) 그리기 (사라지지 않고 상시 대기)
            ctx.strokeStyle = "#00d2ff";
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.arc(bowPos.x - 10, bowPos.y, 35, -Math.PI/2, Math.PI/2);
            ctx.stroke();
            
            // 활시위선
            ctx.strokeStyle = "rgba(255,255,255,0.5)";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(bowPos.x - 10, bowPos.y - 35);
            if(isDragging) ctx.lineTo(dragEnd.x, dragEnd.y);
            else ctx.lineTo(bowPos.x - 10, bowPos.y);
            ctx.lineTo(bowPos.x - 10, bowPos.y + 35);
            ctx.stroke();

            // 대기 중인 화살 시각화 (조건 4-6 사과 화살 디자인 포함)
            if(!isDragging) {
                drawArrowIcon(bowPos.x, bowPos.y, 0, currentArrow.isApple);
            }

            // 드래그 중일 때 조준선 포물선 그리기 (조건 4-1, 4-3 납작하고 빠른 포물선 수학 공식 설계)
            if (isDragging && appleTrajectoryVisible) {
                ctx.save();
                ctx.strokeStyle = currentArrow.isApple ? "#af0404" : "rgba(0, 210, 255, 0.6)";
                ctx.lineWidth = 2;
                ctx.setLineDash([4, 4]); // 점선 형태 구현
                ctx.beginPath();

                let tX = bowPos.x;
                let tY = bowPos.y;
                let tVx = (dragStart.x - dragEnd.x) * 0.25;
                let tVy = (dragStart.y - dragEnd.y) * 0.25;

                ctx.moveTo(tX, tY);
                // 포물선 궤적 시뮬레이션 미리 그리기
                for (let i = 0; i < 40; i++) {
                    tX += tVx;
                    tY += tVy;
                    tVy += currentGravity; // 중력 적용 공식
                    ctx.lineTo(tX, tY);
                    if(tX > canvas.width || tY > canvas.height || tY < 0) break;
                }
                ctx.stroke();
                ctx.restore();

                // 조준 화살 방향 표시
                let angle = Math.atan2(dragStart.y - dragEnd.y, dragStart.x - dragEnd.x);
                drawArrowIcon(dragEnd.x, dragEnd.y, angle, currentArrow.isApple);
            }

            // 3. 날아가는 화살들 물리 엔진 연산 및 그리기
            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                
                if (!arrow.collided) {
                    arrow.x += arrow.vx;
                    arrow.y += arrow.vy;
                    arrow.vy += currentGravity; // 실시간 행성 중력 가속도 추가
                }

                // 화살 각도 계산
                let arrowAngle = Math.atan2(arrow.vy, arrow.vx);

                // 화살 렌더링
                drawArrowIcon(arrow.x, arrow.y, arrowAngle, arrow.isApple, arrow.width);

                // 화면 이탈 검사
                if (arrow.x > canvas.width + 100 || arrow.y > canvas.height + 100 || arrow.x < -100) {
                    activeArrows.splice(i, 1);
                    continue;
                }

                // 과녁 충돌 판정 (화살 끝 부분 기준 수학적 거리 연산)
                if (!arrow.collided) {
                    let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                    let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);
                    
                    let dist = Math.hypot(arrowTipX - target.x, arrowTipY - target.y);

                    if (dist <= target.radiusD) {
                        arrow.collided = true;
                        // 점수 계산 판정 (과녁 안쪽 영역부터 검사)
                        let earnedPoints = 0;
                        if (dist <= target.radiusA) {
                            earnedPoints = 10;
                        } else if (dist <= target.radiusB) {
                            earnedPoints = 5;
                        } else if (dist <= target.radiusC) {
                            earnedPoints = 2;
                        } else {
                            earnedPoints = 1;
                        }

                        // 사과 화살 2배 보너스 적용 조건 처리
                        if(arrow.isApple) {
                            earnedPoints *= 2;
                        }

                        score += earnedPoints;
                        document.getElementById('score-disp').innerText = score;
                        
                        // 맞춘 화살은 과녁과 함께 사라지거나 이탈하게 제거 처리
                        activeArrows.splice(i, 1);
                    }
                }
            }

            gameInterval = requestAnimationFrame(update);
        }

        // 정교한 화살 오브젝트 드로잉 함수
        function drawArrowIcon(x, y, angle, isApple, customWidth) {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(angle);

            let width = customWidth || (canvas.width / 16);
            
            // 화살대 그리기
            ctx.strokeStyle = isApple ? "#ff3333" : "#e2e8f0";
            ctx.lineWidth = isApple ? 4 : 3;
            ctx.beginPath();
            ctx.moveTo(-width/2, 0);
            ctx.lineTo(width/2, 0);
            ctx.stroke();

            // 화살촉 (삼각형)
            ctx.fillStyle = isApple ? "#ff0000" : "#cbd5e1";
            ctx.beginPath();
            ctx.moveTo(width/2, 0);
            ctx.lineTo(width/2 - 10, -6);
            ctx.lineTo(width/2 - 10, 6);
            ctx.closePath();
            ctx.fill();

            // 화살 깃털 고물 (깃)
            ctx.fillStyle = isApple ? "#ffcc00" : "#3182ce";
            ctx.beginPath();
            ctx.moveTo(-width/2, 0);
            ctx.lineTo(-width/2 - 6, -8);
            ctx.lineTo(-width/2 + 4, -8);
            ctx.lineTo(-width/2 + 10, 0);
            ctx.lineTo(-width/2 + 4, 8);
            ctx.lineTo(-width/2 - 6, 8);
            ctx.closePath();
            ctx.fill();

            // 20분의 1 사과 화살 전용 오브젝트 매핑
            if(isApple) {
                ctx.fillStyle = "#fa5252"; // 사과 몸통
                ctx.beginPath();
                ctx.arc(0, -2, 8, 0, Math.PI*2);
                ctx.fill();
                // 사과 꼭지
                ctx.strokeStyle = "#868e96";
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(0, -10);
                ctx.quadraticCurveTo(3, -14, 5, -13);
                ctx.stroke();
            }

            ctx.restore();
        }
    </script>
</body>
</html>
"""

# 스트림릿 컴포넌트로 HTML 주입 (크기 조절)
components.html(game_html, height=620, width=850, scrolling=False)
