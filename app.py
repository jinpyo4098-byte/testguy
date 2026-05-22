import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 기본 설정 (넓은 화면 사용)
st.set_page_config(layout="wide", page_title="Gravity Arrow")

# HTML/JS/CSS 통합 게임 코드
html_game_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gravity Arrow</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            user-select: none;
            /* 기본 지구 지표면 느낌의 배경 (하늘 60%, 땅 40%) */
            background: linear-gradient(to bottom, #87CEEB 60%, #228B22 60%);
            transition: background 0.5s ease;
        }

        /* 메인 타이틀 및 Start 버튼 (중앙) */
        #main-menu {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            z-index: 10;
        }
        #main-menu h1 {
            font-size: 5rem;
            color: white;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
            margin: 0 0 20px 0;
        }
        #start-btn {
            padding: 15px 50px;
            font-size: 1.5rem;
            font-weight: bold;
            background-color: #ff9800;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            transition: transform 0.1s;
        }
        #start-btn:active {
            transform: scale(0.95);
        }

        /* 좌측 상단 행성 버튼 5개 */
        #planet-buttons {
            position: absolute;
            top: 20px;
            left: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            z-index: 10;
        }
        .planet-btn {
            padding: 10px;
            font-size: 1rem;
            font-weight: bold;
            background-color: rgba(255, 255, 255, 0.8);
            border: 2px solid #333;
            border-radius: 5px;
            cursor: pointer;
        }
        .planet-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .planet-btn.active {
            background-color: #333;
            color: white;
            border-color: white;
        }

        /* 우측 상단 최고 기록 */
        #high-score-box {
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 1.5rem;
            font-weight: bold;
            color: white;
            background: rgba(0, 0, 0, 0.6);
            padding: 10px 20px;
            border-radius: 8px;
            z-index: 10;
        }

        /* 게임 중 상단 중앙 스탯 표시 (점수, 시간, 중력) */
        #game-stats {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 30px;
            font-size: 1.5rem;
            font-weight: bold;
            color: white;
            background: rgba(0, 0, 0, 0.6);
            padding: 10px 30px;
            border-radius: 8px;
            z-index: 10;
            visibility: hidden; /* 시작 전엔 숨김 */
        }
        .stat-highlight {
            color: #ffeb3b;
        }

        canvas {
            display: block;
            width: 100vw;
            height: 100vh;
        }
    </style>
</head>
<body>

    <div id="planet-buttons">
        <button class="planet-btn active" data-idx="0">지구</button>
        <button class="planet-btn" data-idx="1">달</button>
        <button class="planet-btn" data-idx="2">화성</button>
        <button class="planet-btn" data-idx="3">금성</button>
        <button class="planet-btn" data-idx="4">유로파</button>
    </div>

    <div id="main-menu">
        <h1>Gravity Arrow</h1>
        <button id="start-btn">Start</button>
    </div>

    <div id="high-score-box">
        최고 기록: <span id="high-score-val">0</span>
    </div>

    <div id="game-stats">
        <div>시간: <span id="time-val" class="stat-highlight">15</span>초</div>
        <div>점수: <span id="score-val" class="stat-highlight">0</span>점</div>
        <div>중력: <span id="gravity-val" class="stat-highlight">9.8</span> m/s²</div>
    </div>

    <canvas id="gameCanvas"></canvas>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            target.baseY = canvas.height * 0.4; // 과녁을 하늘 쪽에 배치
            bow.y = canvas.height * 0.55; // 활을 지표면 근처에 배치
            target.x = canvas.width - 200;
        }
        window.addEventListener('resize', resizeCanvas);

        // 3-6. 행성 데이터 (지표면 느낌의 linear-gradient 배경)
        const planets = [
            { name: '지구', gravity: 9.8, bg: 'linear-gradient(to bottom, #87CEEB 60%, #228B22 60%)' },
            { name: '달',   gravity: 1.6, bg: 'linear-gradient(to bottom, #050505 60%, #555555 60%)' },
            { name: '화성', gravity: 3.7, bg: 'linear-gradient(to bottom, #c08060 60%, #8b4513 60%)' },
            { name: '금성', gravity: 8.9, bg: 'linear-gradient(to bottom, #d4a373 60%, #a0522d 60%)' },
            { name: '유로파', gravity: 1.3, bg: 'linear-gradient(to bottom, #0a192f 60%, #b2ebf2 60%)' }
        ];

        let currentPlanetIdx = 0;
        let score = 0;
        let highScore = 0;
        let timeLeft = 15;
        let isPlaying = false;
        let gameTimer = null;

        // 물리, 오브젝트 변수
        const bow = { x: 150, y: 0 };
        let isDragging = false;
        let dragStart = { x: 0, y: 0 };
        let dragCurrent = { x: 0, y: 0 };
        
        let arrows = [];
        let nextIsApple = false;
        let appleTimer = 0; // 사과 화살 점선 1초 변경 타이머
        let globalTime = 0; // 1초 계산을 위한 누적 시간

        // 과녁 데이터 (A:10, B:5, C:2, D:1)
        const target = {
            x: 0, y: 0, baseY: 0,
            direction: 1, 
            speed: 1.5,
            dirTimer: 0, // 5초 방향 전환용
            rings: [
                { name: 'D', r: 80, score: 1, color: '#ffffff' },
                { name: 'C', r: 55, score: 2, color: '#03a9f4' },
                { name: 'B', r: 30, score: 5, color: '#f44336' },
                { name: 'A', r: 12, score: 10, color: '#ffeb3b' }
            ]
        };

        // UI 요소
        const planetBtns = document.querySelectorAll('.planet-btn');
        const startBtn = document.getElementById('start-btn');
        const mainMenu = document.getElementById('main-menu');
        const gameStats = document.getElementById('game-stats');
        const scoreVal = document.getElementById('score-val');
        const timeVal = document.getElementById('time-val');
        const gravityVal = document.getElementById('gravity-val');
        const highScoreVal = document.getElementById('high-score-val');

        // 초기 세팅
        resizeCanvas();

        // 행성 선택 이벤트
        planetBtns.forEach((btn, idx) => {
            btn.addEventListener('click', () => {
                if (isPlaying) return; // 3-3. 게임 시작되면 배경 못 바꿈
                
                currentPlanetIdx = idx;
                document.body.style.background = planets[idx].bg;
                gravityVal.textContent = planets[idx].gravity.toFixed(1);
                
                planetBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });

        // 게임 시작 이벤트
        startBtn.addEventListener('click', () => {
            isPlaying = true;
            score = 0;
            timeLeft = 15;
            arrows = [];
            target.y = target.baseY;
            target.dirTimer = 0;
            
            scoreVal.textContent = score;
            timeVal.textContent = timeLeft;
            
            mainMenu.style.display = 'none';
            gameStats.style.visibility = 'visible';
            
            // 행성 버튼 비활성화
            planetBtns.forEach(btn => btn.disabled = true);
            
            checkAppleArrow();

            gameTimer = setInterval(() => {
                timeLeft--;
                timeVal.textContent = timeLeft;
                if (timeLeft <= 0) endGame();
            }, 1000);
        });

        function endGame() {
            isPlaying = false;
            clearInterval(gameTimer);
            if (score > highScore) {
                highScore = score;
                highScoreVal.textContent = highScore;
            }
            alert(`게임 종료! 점수: ${score}점`);
            
            mainMenu.style.display = 'block';
            gameStats.style.visibility = 'hidden';
            planetBtns.forEach(btn => btn.disabled = false); // 행성 버튼 다시 활성화
        }

        // 4-6. 1/20 확률 사과 화살
        function checkAppleArrow() {
            nextIsApple = Math.random() < 0.05; 
        }

        // 조작 이벤트
        window.addEventListener('mousedown', (e) => {
            if (!isPlaying) return;
            let dist = Math.hypot(e.clientX - bow.x, e.clientY - bow.y);
            if (dist < 80) {
                isDragging = true;
                dragStart = { x: bow.x, y: bow.y };
                dragCurrent = { x: e.clientX, y: e.clientY };
            }
        });
        window.addEventListener('mousemove', (e) => {
            if (isDragging) dragCurrent = { x: e.clientX, y: e.clientY };
        });
        window.addEventListener('mouseup', () => {
            if (!isDragging) return;
            isDragging = false;

            let dx = dragStart.x - dragCurrent.x;
            let dy = dragStart.y - dragCurrent.y;
            
            // 4-2. 기본 속도 5, 화살이므로 조금 빠른 척도 적용
            let power = Math.hypot(dx, dy) * 0.15; 
            let angle = Math.atan2(dy, dx);

            if (power > 1) { 
                arrows.push({
                    x: bow.x, y: bow.y,
                    vx: Math.cos(angle) * (5 + power),
                    vy: Math.sin(angle) * (5 + power),
                    isApple: nextIsApple,
                    hit: false
                });
                // 4-4. 바로 다음 화살 준비
                checkAppleArrow();
            }
        });

        // 렌더링 루프
        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            let planet = planets[currentPlanetIdx];

            if (isPlaying) {
                // 2-4, 2-5. 과녁 위아래 천천히 이동 (5초마다 방향 전환)
                target.dirTimer += 1/60;
                if (target.dirTimer >= 5) {
                    target.direction *= -1;
                    target.dirTimer = 0;
                }
                target.y += target.speed * target.direction;
                
                // 하늘 밖으로 나가지 않게 제한
                if (target.y < 100 || target.y > canvas.height * 0.6) {
                    target.direction *= -1;
                    target.dirTimer = 0;
                }
                
                globalTime += 1/60;
            }

            // 1. 활 (고정)
            ctx.beginPath();
            ctx.arc(bow.x, bow.y, 40, -Math.PI/2, Math.PI/2);
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 4;
            ctx.stroke();

            // 2. 포물선 및 준비된 화살
            if (isDragging) {
                let dx = bow.x - dragCurrent.x;
                let dy = bow.y - dragCurrent.y;
                let power = Math.hypot(dx, dy) * 0.15;
                let angle = Math.atan2(dy, dx);

                let simVx = Math.cos(angle) * (5 + power);
                let simVy = Math.sin(angle) * (5 + power);
                let simX = bow.x;
                let simY = bow.y;
                
                // 스케일링 된 중력
                let g = planet.gravity * 0.03; 

                ctx.beginPath();
                
                // 4-6. 사과 화살일 경우 1초마다 점선 변경
                if (nextIsApple) {
                    // 1초 단위로 true/false 스위칭
                    if (Math.floor(globalTime) % 2 === 0) {
                        ctx.setLineDash([15, 5]);
                    } else {
                        ctx.setLineDash([5, 15]);
                    }
                } else {
                    ctx.setLineDash([8, 8]);
                }

                for (let i = 0; i < 40; i++) {
                    ctx.lineTo(simX, simY);
                    simX += simVx;
                    // 4-1, 4-3. 화살이므로 너무 직선/포물선이 되지 않게 중력 완화 및 공기저항
                    simVy += g * 0.6; 
                    simVx *= 0.99; 
                }
                ctx.strokeStyle = nextIsApple ? '#ffeb3b' : 'rgba(255, 255, 255, 0.7)';
                ctx.lineWidth = 2;
                ctx.stroke();
                ctx.setLineDash([]);
                
                drawArrow(dragCurrent.x, dragCurrent.y, angle, nextIsApple);
            } else if (isPlaying) {
                drawArrow(bow.x, bow.y, 0, nextIsApple);
            }

            // 3. 날아가는 화살 처리
            for (let i = arrows.length - 1; i >= 0; i--) {
                let a = arrows[i];
                if (!a.hit) {
                    a.vy += planet.gravity * 0.03 * 0.6; // 실제 중력 적용 (완화됨)
                    a.x += a.vx;
                    a.y += a.vy;

                    // 과녁 충돌 확인
                    let distToTarget = Math.hypot(a.x - target.x, a.y - target.y);
                    if (distToTarget <= target.rings[0].r) {
                        a.hit = true;
                        let hitScore = 0;
                        for (let j = target.rings.length - 1; j >= 0; j--) {
                            if (distToTarget <= target.rings[j].r) {
                                hitScore = target.rings[j].score;
                                break;
                            }
                        }
                        
                        if (a.isApple) hitScore *= 2; // 사과 화살 2배
                        
                        score += hitScore;
                        scoreVal.textContent = score;
                    }
                }
                
                drawArrow(a.x, a.y, Math.atan2(a.vy, a.vx), a.isApple);
                
                // 화면 밖 화살 삭제
                if (a.x > canvas.width + 100 || a.y > canvas.height + 100 || a.x < -100) {
                    arrows.splice(i, 1);
                }
            }

            // 4. 과녁 그리기 (역순으로 그려 작은 원이 위로 오게)
            target.rings.forEach(ring => {
                ctx.beginPath();
                ctx.arc(target.x, target.y, ring.r, 0, Math.PI * 2);
                ctx.fillStyle = ring.color;
                ctx.fill();
                ctx.strokeStyle = '#000';
                ctx.stroke();
            });

            requestAnimationFrame(gameLoop);
        }

        // 화살 그리기 함수
        function drawArrow(x, y, angle, isApple) {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(angle);

            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            
            // 화살대
            ctx.beginPath();
            ctx.moveTo(-20, 0);
            ctx.lineTo(15, 0);
            ctx.stroke();
            
            // 화살촉
            ctx.beginPath();
            ctx.moveTo(15, 0);
            ctx.lineTo(5, -5);
            ctx.lineTo(5, 5);
            ctx.closePath();
            ctx.fillStyle = isApple ? '#ff5722' : '#fff';
            ctx.fill();

            // 사과 장식
            if (isApple) {
                ctx.beginPath();
                ctx.arc(0, 0, 5, 0, Math.PI * 2);
                ctx.fillStyle = '#f44336'; // 빨간 사과
                ctx.fill();
            }

            ctx.restore();
        }

        requestAnimationFrame(gameLoop);
    </script>
</body>
</html>
"""

# Streamlit에 HTML 렌더링 (스크롤바 없애고 전체화면 크기로)
components.html(html_game_code, height=850, scrolling=False)
