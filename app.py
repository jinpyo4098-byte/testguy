import streamlit as st
import streamlit.components.v1 as components

# 스트림릿 페이지 설정 (여백 제거)
st.set_page_config(page_title="Gravity Arrow", layout="wide")
st.markdown(
    """
    <style>
    .reportview-container .main .block-container{ max-width: 100%; padding: 0; }
    iframe { display: block; width: 100vw; height: 98vh; border: none; }
    body { margin: 0; }
    </style>
    """,
    unsafe_allow_html=True
)

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gravity Arrow</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: radial-gradient(circle, #161f2b 0%, #050608 100%);
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            user-select: none;
        }

        #game-wrapper {
            position: relative;
            width: 100vw;
            height: 100vh;
        }

        #game-canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: transparent;
            cursor: crosshair;
            z-index: 1;
        }

        .screen-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: rgba(5, 6, 8, 0.9);
            z-index: 10;
        }

        .hidden {
            display: none !important;
        }

        h1 {
            font-size: 4.5rem;
            margin: 10px 0;
            text-shadow: 0 0 20px #00d2ff;
            font-weight: 800;
            letter-spacing: 3px;
        }

        .result-title {
            font-size: 3.5rem;
            color: #ffcc00;
            text-shadow: 0 0 15px #ffcc00;
            margin-bottom: 20px;
        }

        .score-report {
            font-size: 2rem;
            margin-bottom: 45px;
            text-align: center;
            line-height: 1.6;
        }

        /* 인게임 상태창 UI 패널 */
        .ui-panel {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 60%;
            max-width: 700px;
            background: rgba(255, 255, 255, 0.07);
            padding: 15px 30px;
            border-radius: 25px;
            box-sizing: border-box;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            z-index: 5;
        }

        .stats {
            font-size: 1.4rem;
            font-weight: bold;
            letter-spacing: 1px;
            margin-bottom: 10px;
            width: 100%;
            text-align: center;
        }

        /* 시간 게이지바 컨테이너 */
        .progress-container {
            width: 100%;
            height: 14px;
            background-color: rgba(255, 255, 255, 0.15);
            border-radius: 7px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* 시간 게이지바 본체 */
        .progress-bar {
            height: 100%;
            width: 100%;
            background: linear-gradient(90deg, #0066ff, #00d2ff);
            box-shadow: 0 0 10px #00d2ff;
            transition: width 0.1s linear, background 0.3s;
        }

        /* 폭주/버프 상태일 때 게이지 컬러 체인지 연출 */
        .progress-bar.buffed {
            background: linear-gradient(90deg, #ff0055, #ffcc00) !important;
            box-shadow: 0 0 15px #ff0055 !important;
        }

        .btn {
            background: linear-gradient(135deg, #00d2ff 0%, #0066ff 100%);
            border: none;
            color: white;
            padding: 18px 45px;
            font-size: 1.5rem;
            font-weight: bold;
            border-radius: 35px;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 20px rgba(0, 102, 255, 0.4);
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(0, 132, 255, 0.6);
        }

        .main-planet-selector {
            display: flex;
            gap: 20px;
            align-items: center;
            margin-bottom: 40px;
            background: rgba(255, 255, 255, 0.05);
            padding: 20px 35px;
            border-radius: 50px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .planet-circle {
            width: 65px;
            height: 65px;
            border-radius: 50%;
            cursor: pointer;
            border: 3px solid transparent;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            font-weight: bold;
            text-shadow: 1px 1px 2px #000;
        }

        .planet-circle:hover {
            transform: scale(1.15);
        }

        .planet-circle.active {
            border-color: #fff;
            box-shadow: 0 0 22px currentColor;
            transform: scale(1.05);
        }

        #planet-earth { background: radial-gradient(circle at 30% 30%, #2b82c9, #053057); color: #00d2ff; }
        #planet-moon { background: radial-gradient(circle at 30% 30%, #ccc, #666); color: #ddd; }
        #planet-mars { background: radial-gradient(circle at 30% 30%, #e03e1d, #5c1303); color: #ff6b6b; }
        #planet-venus { background: radial-gradient(circle at 30% 30%, #e3a857, #6d3e00); color: #ffd166; }
        #planet-europa { background: radial-gradient(circle at 30% 30%, #a5cad6, #3a5d6b); color: #98e1f5; }

        #combo-wrapper {
            position: absolute;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 5;
            text-align: center;
            pointer-events: none;
        }
        
        .combo-text {
            font-size: 3rem;
            font-weight: 900;
            font-style: italic;
            color: #ff3e3e;
            text-shadow: 0 0 10px rgba(255, 62, 62, 0.8), 0 0 20px rgba(255, 200, 0, 0.5);
            margin: 0;
        }

        /* 능력 활성화 알림 오버레이 텍스트 스타일 */
        #buff-alert {
            position: absolute;
            top: 120px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 2.2rem;
            font-weight: bold;
            color: #ffcc00;
            text-shadow: 0 0 15px #ff3300;
            z-index: 5;
            pointer-events: none;
            letter-spacing: 2px;
            background: rgba(0,0,0,0.5);
            padding: 8px 25px;
            border-radius: 15px;
        }
    </style>
</head>
<body>

    <div id="game-wrapper">
        
        <div id="start-screen" class="screen-overlay">
            <h1>Gravity Arrow</h1>
            <p style="font-size: 1.4rem; color: #a0aec0; margin-bottom: 30px;">행성을 선택하고 15초에 등장하는 운석을 파괴해 각성하세요!</p>
            
            <div class="main-planet-selector" id="planet-selector-bar">
                <div id="planet-earth" class="planet-circle active" onclick="selectPlanet('earth')">지구</div>
                <div id="planet-moon" class="planet-circle" onclick="selectPlanet('moon')">달</div>
                <div id="planet-mars" class="planet-circle" onclick="selectPlanet('mars')">화성</div>
                <div id="planet-venus" class="planet-circle" onclick="selectPlanet('venus')">금성</div>
                <div id="planet-europa" class="planet-circle" onclick="selectPlanet('europa')">유로파</div>
            </div>

            <button class="btn" onclick="startGame()">게임 시작</button>
            <p style="font-size: 1.1rem; color: #718096; margin-top: 25px;">최고 기록: <span id="main-high-disp" style="color:#00d2ff;">0</span>점</p>
        </div>

        <div id="ingame-ui" class="ui-panel hidden">
            <div class="stats">
                행성: <span id="planet-name-disp" style="color:#ffcc00;">지구</span> | 
                점수: <span id="score-disp" style="color:#00d2ff;">0</span>
            </div>
            <div class="progress-container">
                <div id="time-progress" class="progress-bar"></div>
            </div>
        </div>

        <div id="buff-alert" class="hidden">🔥 과녁 증폭 및 감속 활성화! 🔥</div>

        <div id="combo-wrapper" class="hidden">
            <p class="combo-text" id="combo-disp">5 COMBO</p>
        </div>

        <div id="result-screen" class="screen-overlay hidden">
            <div class="result-title" id="result-title-text">GAME OVER</div>
            <div class="score-report">
                최종 점수: <span id="final-score-disp" style="color: #00d2ff; font-weight: bold;">0</span> 점<br>
                최대 콤보: <span id="final-combo-disp" style="color: #ff3e3e; font-weight: bold;">0</span> 콤보<br>
                <span id="highscore-message" style="font-size: 1.4rem; color: #4cdf50;"></span>
            </div>
            <button class="btn" onclick="goToMain()">메인으로 가기</button>
        </div>

        <canvas id="game-canvas"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            
            bowPos.x = 120; 
            bowPos.y = canvas.height / 2;
            target.x = canvas.width - 150; 
        }

        const planets = {
            earth: { name: '지구', gravity: 9.8, color: '#2b82c9' },
            moon: { name: '달', gravity: 1.6, color: '#ccc' },
            mars: { name: '화성', gravity: 3.7, color: '#e03e1d' },
            venus: { name: '금성', gravity: 8.9, color: '#e3a857' },
            europa: { name: '유로파', gravity: 1.3, color: '#a5cad6' }
        };
        const planetKeys = ['earth', 'moon', 'mars', 'venus', 'europa'];
        let currentPlanetKey = 'earth';

        // 게임 제어 변수
        let score = 0;
        let highScore = localStorage.getItem('gravity_arrow_high') || 0;
        const totalDuration = 30; // 총 30초 게임
        let timeLeft = 30;
        let gameActive = false;
        let gameInterval;
        let timerInterval;

        // 버프(능력구현) 및 특수 오브젝트 관련 데이터
        let buffTimer = 0; // 버프 지속 프레임 타이머
        let isBuffed = false;

        // 운석 객체 데이터 구조 설계
        let meteor = {
            x: 0,
            y: 0,
            vx: 0,
            vy: 0,
            radius: 45,
            active: false,
            destroyed: false
        };

        // 과녁 세팅 전역변수화 관리
        let target = {
            x: window.innerWidth - 150,
            y: window.innerHeight / 2,
            baseRadiusD: 85, 
            radiusD: 85, radiusC: 62, radiusB: 38, radiusA: 15,  
            baseSpeed: 2.5,
            speed: 2.5,
            dir: 1,
            visible: true,
            respawnTimer: 0
        };

        let combo = 0;
        let maxCombo = 0;
        let shakeIntensity = 0;
        let particles = [];
        let scoreTexts = [];

        let gravityScale = 0.03; 
        let currentGravity = planets[currentPlanetKey].gravity * gravityScale;

        // 궁수(사람) 상태 및 외형 관리 데이터
        const bowPos = { x: 120, y: window.innerHeight / 2 };
        let isDragging = false;
        let dragStart = { x: 0, y: 0 };
        let dragEnd = { x: 0, y: 0 };
        
        let activeArrows = [];
        let currentArrow = { isApple: false };
        let appleTimer = 0;
        let appleTrajectoryVisible = true;

        document.getElementById('main-high-disp').innerText = highScore;
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        function selectPlanet(key) {
            if (gameActive) return; 
            currentPlanetKey = key;
            planetKeys.forEach(k => {
                document.getElementById(`planet-${k}`).classList.remove('active');
            });
            document.getElementById(`planet-${key}`).classList.add('active');
            
            document.getElementById('planet-name-disp').innerText = planets[key].name;
            currentGravity = planets[key].gravity * gravityScale;
            
            generateStars(); 
        }

        function startGame() {
            score = 0;
            timeLeft = totalDuration; 
            combo = 0;
            maxCombo = 0;
            gameActive = true;
            activeArrows = [];
            particles = [];
            scoreTexts = [];
            
            isBuffed = false;
            buffTimer = 0;
            document.getElementById('buff-alert').classList.add('hidden');
            document.getElementById('time-progress').classList.remove('buffed');

            // 과녁 상태 복구 원상복귀
            target.visible = true;
            target.respawnTimer = 0;
            resetTargetSpecification(false);

            // 운석 리셋
            meteor.active = false;
            meteor.destroyed = false;

            document.getElementById('start-screen').classList.add('hidden');
            document.getElementById('result-screen').classList.add('hidden');
            document.getElementById('combo-wrapper').classList.add('hidden');
            document.getElementById('ingame-ui').classList.remove('hidden');

            document.getElementById('score-disp').innerText = score;
            updateProgressBar();

            let targetDirInterval = setInterval(() => {
                if(!gameActive) clearInterval(targetDirInterval);
                target.dir *= -1;
            }, 4500);

            timerInterval = setInterval(() => {
                timeLeft--;
                updateProgressBar();

                // 정확히 15초가 되었을 때 운석 리스폰 작동 개시
                if(timeLeft === 15 && !meteor.destroyed) {
                    spawnMeteor();
                }

                if(timeLeft <= 0) {
                    endGame();
                }
            }, 1000);

            gameInterval = requestAnimationFrame(update);
        }

        function updateProgressBar() {
            const bar = document.getElementById('time-progress');
            const percentage = (timeLeft / totalDuration) * 100;
            bar.style.width = `${percentage}%`;
        }

        function spawnMeteor() {
            meteor.x = canvas.width + 50;
            meteor.y = 80; // 우측 상단에서 스폰
            
            // 사람(궁수)의 보정 좌표를 향해 날아가도록 속도 연산 제어 (매우 천천히 기어옴)
            let dx = bowPos.x - meteor.x;
            let dy = bowPos.y - meteor.y;
            let distance = Math.hypot(dx, dy);
            
            let slowSpeed = 1.3; // 천천히 비행
            meteor.vx = (dx / distance) * slowSpeed;
            meteor.vy = (dy / distance) * slowSpeed;
            meteor.active = true;
        }

        // 각성 모드 전환에 따른 스펙 설정 함수 구현
        function resetTargetSpecification(buffActive) {
            if(buffActive) {
                target.radiusD = target.baseRadiusD * 1.5; // 과녁 크기 1.5배 확장 증가
                target.radiusC = 62 * 1.5;
                target.radiusB = 38 * 1.5;
                target.radiusA = 15 * 1.5;
                target.speed = target.baseSpeed * 0.4; // 이동 속도 대폭 슬로우 감소 감속 조치
            } else {
                target.radiusD = target.baseRadiusD;
                target.radiusC = 62;
                target.radiusB = 38;
                target.radiusA = 15;
                target.speed = target.baseSpeed;
            }
        }

        function activateAbilityBuff() {
            isBuffed = true;
            buffTimer = 300; // 60fps * 5초 = 300프레임 동안 유지 연산 적용
            resetTargetSpecification(true);
            document.getElementById('buff-alert').classList.remove('hidden');
            document.getElementById('time-progress').classList.add('buffed');
            shakeIntensity = 12;
        }

        function deactivateAbilityBuff() {
            isBuffed = false;
            resetTargetSpecification(false);
            document.getElementById('buff-alert').classList.add('hidden');
            document.getElementById('time-progress').classList.remove('buffed');
        }

        function endGame() {
            gameActive = false;
            cancelAnimationFrame(gameInterval);
            clearInterval(timerInterval);
            
            document.getElementById('ingame-ui').classList.add('hidden');
            document.getElementById('combo-wrapper').classList.add('hidden');
            document.getElementById('buff-alert').classList.add('hidden');

            document.getElementById('final-score-disp').innerText = score;
            document.getElementById('final-combo-disp').innerText = maxCombo;
            const msgElement = document.getElementById('highscore-message');
            const titleElement = document.getElementById('result-title-text');

            if(score > highScore) {
                highScore = score;
                localStorage.setItem('gravity_arrow_high', highScore);
                document.getElementById('main-high-disp').innerText = highScore;
                titleElement.innerText = "NEW RECORD!";
                titleElement.style.color = "#4cdf50";
                msgElement.innerText = "축하합니다! 최고 기록을 경신했습니다!";
            } else {
                titleElement.innerText = "GAME OVER";
                titleElement.style.color = "#ffcc00";
                msgElement.innerText = "";
            }

            document.getElementById('result-screen').classList.remove('hidden');
        }

        function goToMain() {
            document.getElementById('result-screen').classList.add('hidden');
            document.getElementById('start-screen').classList.remove('hidden');
            activeArrows = [];
            particles = [];
            scoreTexts = [];
        }

        function rollNextArrow() {
            currentArrow = { isApple: Math.random() < 0.06 };
            appleTimer = 0;
            appleTrajectoryVisible = true;
        }
        rollNextArrow();

        function createExplosion(x, y, color, customCount) {
            let count = customCount || 15; 
            for (let i = 0; i < count; i++) {
                let angle = Math.random() * Math.PI * 2;
                let speed = 1 + Math.random() * 5;
                particles.push({
                    x: x, y: y,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed,
                    radius: 2 + Math.random() * 4,
                    color: color,
                    alpha: 1,
                    decay: 0.015 + Math.random() * 0.02
                });
            }
        }

        function createScoreText(x, y, text, color) {
            scoreTexts.push({ x: x, y: y, text: text, color: color, alpha: 1, vy: -0.8 });
        }

        function getMousePos(e) {
            return { x: e.clientX, y: e.clientY };
        }

        window.addEventListener('mousedown', (e) => {
            if(!gameActive) return;
            const mousePos = getMousePos(e);
            // 활터 및 사람 캐릭터 조작 영역 보정치 체크 감지
            if(Math.hypot(mousePos.x - bowPos.x, mousePos.y - bowPos.y) < 110) {
                isDragging = true;
                dragStart = { x: bowPos.x, y: bowPos.y };
                dragEnd = { x: mousePos.x, y: mousePos.y };
            }
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            const mousePos = getMousePos(e);
            dragEnd = { x: mousePos.x, y: mousePos.y };
        });

        window.addEventListener('mouseup', (e) => {
            if (!isDragging) return;
            isDragging = false;

            const dx = dragStart.x - dragEnd.x; 
            const dy = dragStart.y - dragEnd.y;
            if (dx <= 0) return; 

            const speedScale = 0.25; 
            const vx = dx * speedScale; 
            const vy = dy * speedScale;

            if(vx > 0) {
                activeArrows.push({
                    x: bowPos.x, y: bowPos.y,
                    vx: vx, vy: vy,
                    isApple: currentArrow.isApple,
                    width: 95, height: 5,
                    collided: false,
                    handled: false 
                });
                rollNextArrow(); 
            }
        });

        let stars = [];
        function generateStars() {
            stars = [];
            let count = Math.floor((window.innerWidth * window.innerHeight) / 25000);
            for(let i=0; i<count; i++) {
                stars.push({x: Math.random()*canvas.width, y: Math.random()*canvas.height, r: Math.random()*1.6});
            }
        }
        generateStars();

        // [사람(궁수) 그리기 함수 벡터 드로잉 구현]
        function drawArcherCharacter(dragOffsetAngle) {
            ctx.save();
            ctx.translate(bowPos.x - 45, bowPos.y); // 위치 이동 설정
            
            // 드래그 세기에 맞춰 상체가 뒤로 기울어지는 틸팅 연출
            let tilt = isDragging ? dragOffsetAngle * 0.4 : 0;
            ctx.rotate(tilt);

            ctx.lineWidth = 3.5;
            ctx.strokeStyle = "#ffffff";
            ctx.fillStyle = "#1e293b";

            // 1. 다리 구조선
            ctx.beginPath();
            ctx.moveTo(-10, 60); ctx.lineTo(-15, 95); // 왼다리
            ctx.moveTo(10, 60); ctx.lineTo(15, 95);  // 오른다리
            ctx.stroke();

            // 2. 몸통 토르소 디자인
            ctx.fillStyle = "#2d3748";
            ctx.beginPath();
            ctx.moveTo(-15, 10); ctx.lineTo(15, 10);
            ctx.lineTo(10, 60); ctx.lineTo(-10, 60);
            ctx.closePath();
            ctx.fill(); ctx.stroke();

            // 3. 머리 헤드
            ctx.fillStyle = "#e2e8f0";
            ctx.beginPath();
            ctx.arc(0, -12, 14, 0, Math.PI*2);
            ctx.fill(); ctx.stroke();

            // 4. 활시위를 당기는 팔 그래픽 표현 제어 루프
            ctx.strokeStyle = "#e2e8f0";
            if(isDragging) {
                // 앞팔 (활 조준 방향 연장선)
                ctx.beginPath();
                ctx.moveTo(12, 22);
                ctx.lineTo(40, 10);
                ctx.stroke();

                // 뒷팔 (시위 당김 가속선)
                ctx.beginPath();
                ctx.moveTo(-12, 22);
                let pullX = (dragEnd.x - dragStart.x) * 0.2;
                let pullY = (dragEnd.y - dragStart.y) * 0.2;
                ctx.lineTo(-25 + pullX, 22 + pullY);
                ctx.stroke();
            } else {
                ctx.beginPath();
                ctx.moveTo(12, 22); ctx.lineTo(35, 15);
                ctx.moveTo(-12, 22); ctx.lineTo(10, 35);
                ctx.stroke();
            }

            ctx.restore();
        }

        function update() {
            // 능력치 유지시간 프레임 차감 연산 진행
            if (gameActive && isBuffed) {
                buffTimer--;
                if(buffTimer <= 0) {
                    deactivateAbilityBuff();
                }
            }

            if (gameActive) {
                // 과녁이 살아있을 때만 움직임 가동
                if(target.visible) {
                    target.y += target.speed * target.dir;
                    if(target.y - target.radiusD < 140 || target.y + target.radiusD > canvas.height - 40) {
                        target.dir *= -1; 
                    }
                } else {
                    // 과녁 소멸 리스폰 대기 연산 타이머 작동 처리
                    target.respawnTimer--;
                    if(target.respawnTimer <= 0) {
                        // 랜덤 y축 지점에 투핑 리스폰 재생성
                        target.y = 180 + Math.random() * (canvas.height - 320);
                        target.visible = true;
                    }
                }

                // 사과 화살 깜빡이 갱신
                if(currentArrow.isApple) {
                    appleTimer++;
                    if(appleTimer % 45 === 0) {
                        appleTrajectoryVisible = !appleTrajectoryVisible;
                    }
                }

                // 운석 이동 물리엔진 연산구간
                if(meteor.active) {
                    meteor.x += meteor.vx;
                    meteor.y += meteor.vy;

                    // 만약 플레이어 캐릭터 위치 근처 한계점에 도달하면 파괴 처리 (피격 실패)
                    if(meteor.x < bowPos.x - 20) {
                        meteor.active = false;
                        createExplosion(meteor.x, meteor.y, "#94a3b8", 30);
                        shakeIntensity = 10;
                    }
                }
            }

            ctx.save();
            if (shakeIntensity > 0) {
                ctx.translate((Math.random() - 0.5) * shakeIntensity, (Math.random() - 0.5) * shakeIntensity);
                shakeIntensity *= 0.85; 
                if (shakeIntensity < 0.2) shakeIntensity = 0;
            }

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 우주 성운 입자 시각화
            ctx.fillStyle = "rgba(255,255,255,0.35)";
            stars.forEach(s => {
                ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill();
            });

            // 각성 버프 모드 돌입 시 붉은색 스크린 연출 처리 필터링
            if(isBuffed && gameActive) {
                ctx.fillStyle = "rgba(255, 62, 62, 0.04)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            // [운석(Meteor) 그리기 섹션 추가]
            if(meteor.active) {
                ctx.save();
                // 네온 방열 이펙트 연출 트레일 테두리 그리기
                ctx.fillStyle = "rgba(239, 68, 68, 0.25)";
                ctx.beginPath(); ctx.arc(meteor.x, meteor.y, meteor.radius + 12 + Math.random()*6, 0, Math.PI*2); ctx.fill();

                // 마그마 본체 스피어 드로잉
                let grad = ctx.createRadialGradient(meteor.x - 10, meteor.y - 10, 5, meteor.x, meteor.y, meteor.radius);
                grad.addColorStop(0, '#ff9e00'); grad.addColorStop(0.6, '#d946ef'); grad.addColorStop(1, '#450a0a');
                ctx.fillStyle = grad;
                ctx.beginPath(); ctx.arc(meteor.x, meteor.y, meteor.radius, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#ff0055"; ctx.lineWidth = 3; ctx.stroke();
                ctx.restore();
            }

            // [과녁 렌더링 - 조건부 투명성 처리 반영]
            const targetColor = planets[currentPlanetKey].color;
            const skewX = 0.25; 
            const frontX = target.x - (target.radiusD * skewX); 
            const backX = target.x + (target.radiusD * skewX); 

            if(target.visible) {
                ctx.save();
                ctx.strokeStyle = "#4a5568"; ctx.lineWidth = 6;
                ctx.beginPath();
                ctx.moveTo(target.x + 5, target.y - target.radiusD); ctx.lineTo(target.x + 5, target.y + target.radiusD);
                ctx.stroke();

                ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, (target.radiusD + 6) * skewX, target.radiusD + 6, 0, 0, Math.PI * 2); ctx.fill();

                ctx.fillStyle = "#ffffff";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusD * skewX, target.radiusD, 0, 0, Math.PI * 2); ctx.fill(); 
                
                ctx.fillStyle = targetColor;
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusC * skewX, target.radiusC, 0, 0, Math.PI * 2); ctx.fill();
                
                ctx.fillStyle = "#ff3e3e";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusB * skewX, target.radiusB, 0, 0, Math.PI * 2); ctx.fill();
                
                ctx.fillStyle = "#ffcc00";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusA * skewX, target.radiusA, 0, 0, Math.PI * 2); ctx.fill();
                ctx.restore();
            }

            // 궁수 캐릭터 연동 인터페이스 로드 구현
            let dragAngle = Math.atan2(dragStart.y - dragEnd.y, dragStart.x - dragEnd.x);
            drawArcherCharacter(dragAngle);

            // 활과 활시위 레이아웃 드로잉 포지션 업데이트 보정
            ctx.save();
            ctx.strokeStyle = isBuffed ? "#ff0055" : "#00d2ff";
            ctx.lineWidth = 5; 
            ctx.beginPath();
            ctx.arc(bowPos.x - 12, bowPos.y, 48, -Math.PI/2, Math.PI/2); 
            ctx.stroke();
            
            ctx.strokeStyle = "rgba(255,255,255,0.5)";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(bowPos.x - 12, bowPos.y - 48);
            if(isDragging) ctx.lineTo(dragEnd.x, dragEnd.y);
            else ctx.lineTo(bowPos.x - 12, bowPos.y);
            ctx.lineTo(bowPos.x - 12, bowPos.y + 48);
            ctx.stroke();
            ctx.restore();

            if(!isDragging && gameActive) {
                drawArrowIcon(bowPos.x, bowPos.y, 0, currentArrow.isApple);
            }

            // 포물선 가이드라인 궤적 트래킹 연산 루프
            if (isDragging && appleTrajectoryVisible && gameActive) {
                let tVx = (dragStart.x - dragEnd.x) * 0.25;
                if (tVx > 0) { 
                    ctx.save();
                    ctx.strokeStyle = currentArrow.isApple ? "#af0404" : "rgba(0, 210, 255, 0.5)";
                    ctx.lineWidth = 2.5; ctx.setLineDash([5, 5]);
                    ctx.beginPath();

                    let tX = bowPos.x; let tY = bowPos.y;
                    let tVy = (dragStart.y - dragEnd.y) * 0.25;

                    ctx.moveTo(tX, tY);
                    for (let i = 0; i < 60; i++) {
                        tX += tVx; tY += tVy; tVy += currentGravity; 
                        ctx.lineTo(tX, tY);
                        if(tX > canvas.width || tY > canvas.height || tY < 0) break;
                    }
                    ctx.stroke(); ctx.restore();

                    drawArrowIcon(dragEnd.x, dragEnd.y, dragAngle, currentArrow.isApple);
                }
            }

            // 화살 배열 투사체 순회 및 처리구간
            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                
                arrow.x += arrow.vx;
                arrow.y += arrow.vy;
                arrow.vy += currentGravity;

                let arrowAngle = Math.atan2(arrow.vy, arrow.vx);
                drawArrowIcon(arrow.x, arrow.y, arrowAngle, arrow.isApple, arrow.width);

                let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);

                // 화면 경계 바깥 탈출 스캔 검사 연산 처리
                if (arrow.x > canvas.width + 50 || arrow.y > canvas.height + 50 || arrow.y < -50) {
                    if(!arrow.handled) {
                        combo = 0; document.getElementById('combo-wrapper').classList.add('hidden');
                    }
                    activeArrows.splice(i, 1);
                    continue;
                }

                // 충돌 처리 루프 1단계: 특수 운석 충돌 트래킹 검증
                if(meteor.active) {
                    let distToMeteor = Math.hypot(arrowTipX - meteor.x, arrowTipY - meteor.y);
                    if(distToMeteor <= meteor.radius + 10) {
                        meteor.active = false;
                        meteor.destroyed = true;
                        activeArrows.splice(i, 1); // 투사체 소멸

                        createExplosion(meteor.x, meteor.y, "#ffcc00", 40);
                        createScoreText(meteor.x, meteor.y, "AWAKENING!!", "#ffcc00");
                        
                        // 각성 버프 패시브 능력 활성화 가동 스위치 온
                        activateAbilityBuff();
                        continue;
                    }
                }

                // 충돌 처리 루프 2단계: 메인 과녁 충돌 트래킹 감지 검사 (과녁이 눈에 보일 때만 판정 인정)
                if (target.visible && arrowTipX >= frontX && arrowTipX <= backX + 15 && arrow.vx > 0) {
                    let dy = Math.abs(arrowTipY - target.y);

                    if (dy <= target.radiusD) {
                        arrow.handled = true;
                        
                        // [요청 수정사항 핵심]: 화살 고정 삭제 대신 과녁 소멸 트리거 발동 처리 기믹 가동
                        target.visible = false;
                        target.respawnTimer = 45; // 45프레임 뒤 재배치 재생성 처리 지시

                        combo++;
                        if(combo > maxCombo) maxCombo = combo;
                        
                        document.getElementById('combo-disp').innerText = `${combo} COMBO`;
                        document.getElementById('combo-wrapper').classList.remove('hidden');

                        let earnedPoints = 0;
                        let hColor = "#ffffff";
                        
                        if (dy <= target.radiusA) { earnedPoints = 10; hColor = "#ffcc00"; }
                        else if (dy <= target.radiusB) { earnedPoints = 5;  hColor = "#ff3e3e"; }
                        else if (dy <= target.radiusC) { earnedPoints = 2;  hColor = targetColor; }
                        else { earnedPoints = 1;  hColor = "#e2e8f0"; }

                        if(arrow.isApple) { earnedPoints *= 2; hColor = "#ff2222"; }

                        let totalEarned = earnedPoints + Math.floor(combo / 3);
                        score += totalEarned;
                        document.getElementById('score-disp').innerText = score;

                        createScoreText(arrowTipX - 25, arrowTipY - 15, `+${totalEarned}`, hColor);
                        shakeIntensity = 7; 
                        createExplosion(arrowTipX, arrowTipY, hColor, 20);

                        activeArrows.splice(i, 1); // 화살은 바로 소거 처리
                        continue;
                    }
                }
            }

            // 파티클 엔진
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.x += p.vx; p.y += p.vy; p.alpha -= p.decay;
                if (p.alpha <= 0) { particles.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = p.alpha; ctx.fillStyle = p.color;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI*2); ctx.fill(); ctx.restore();
            }

            // 스코어 보정용 부유 텍스트
            for (let i = scoreTexts.length - 1; i >= 0; i--) {
                let stx = scoreTexts[i];
                stx.y += stx.vy; stx.alpha -= 0.015;
                if(stx.alpha <= 0) { scoreTexts.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = stx.alpha; ctx.fillStyle = stx.color;
                ctx.font = "bold 26px 'Segoe UI'"; ctx.shadowColor = "rgba(0,0,0,0.5)"; ctx.shadowBlur = 4;
                ctx.fillText(stx.text, stx.x, stx.y); ctx.restore();
            }

            ctx.restore(); 
            gameInterval = requestAnimationFrame(update);
        }

        function drawArrowIcon(x, y, angle, isApple, customWidth) {
            ctx.save();
            ctx.translate(x, y); ctx.rotate(angle);
            let width = customWidth || 95; 
            
            ctx.strokeStyle = isApple ? "#ff3333" : "#e2e8f0";
            ctx.lineWidth = isApple ? 5.5 : 4.5; 
            ctx.beginPath(); ctx.moveTo(-width/2, 0); ctx.lineTo(width/2, 0); ctx.stroke();

            ctx.fillStyle = isApple ? "#ff0000" : "#cbd5e1";
            ctx.beginPath(); ctx.moveTo(width/2, 0); ctx.lineTo(width/2 - 15, -8); ctx.lineTo(width/2 - 15, 8); ctx.closePath(); ctx.fill();

            ctx.fillStyle = isApple ? "#ffcc00" : "#3182ce";
            ctx.beginPath(); ctx.moveTo(-width/2, 0); ctx.lineTo(-width/2 - 8, -10); ctx.lineTo(-width/2 + 5, -10); ctx.lineTo(-width/2 + 12, 0); ctx.lineTo(-width/2 + 5, 10); ctx.lineTo(-width/2 - 8, 10); ctx.closePath(); ctx.fill();

            if(isApple) {
                ctx.fillStyle = "#fa5252"; ctx.beginPath(); ctx.arc(0, -4, 11, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#868e96"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(0, -14); ctx.quadraticCurveTo(3, -19, 6, -17); ctx.stroke();
            }
            ctx.restore();
        }

        update();
    </script>
</body>
</html>
"""

components.html(game_html, height=850, scrolling=False)
