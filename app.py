<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>우주 양궁 게임 (Planet Archery)</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background-color: #1a202c;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            user-select: none;
        }
        canvas {
            display: block;
            width: 100vw;
            height: 100vh;
        }
        #ui-layer {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .header {
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        .score-box {
            background: rgba(0, 0, 0, 0.6);
            padding: 10px 20px;
            border-radius: 12px;
            border: 2px solid #4a5568;
            pointer-events: auto;
        }
        .score-box h1 { margin: 0; font-size: 24px; color: #e2e8f0; }
        .score-box span { color: #ffcc00; font-size: 32px; font-weight: bold; }
        
        .planet-selector {
            display: flex;
            gap: 10px;
            pointer-events: auto;
        }
        .planet-btn {
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid #4a5568;
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.2s;
        }
        .planet-btn:hover { background: #2d3748; }
        .planet-btn.active { border-color: #ffcc00; color: #ffcc00; box-shadow: 0 0 10px rgba(255, 204, 0, 0.5); }
        
        #combo-wrapper {
            position: absolute;
            top: 40%; left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            opacity: 1;
            transition: opacity 0.5s;
        }
        #combo-wrapper.hidden { opacity: 0; }
        #combo-disp {
            font-size: 60px;
            font-weight: 900;
            color: #ff3e3e;
            text-shadow: 0 0 15px rgba(255, 62, 62, 0.8), 2px 2px 0 #000;
            margin: 0;
            animation: pop 0.2s ease-out;
        }
        @keyframes pop {
            0% { transform: scale(0.5); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div id="ui-layer">
        <div class="header">
            <div class="score-box">
                <h1>SCORE: <span id="score-disp">0</span></h1>
            </div>
            <div class="planet-selector">
                <button class="planet-btn active" onclick="changePlanet('earth')">지구</button>
                <button class="planet-btn" onclick="changePlanet('moon')">달</button>
                <button class="planet-btn" onclick="changePlanet('mars')">화성</button>
                <button class="planet-btn" onclick="changePlanet('venus')">금성</button>
                <button class="planet-btn" onclick="changePlanet('europa')">유로파</button>
            </div>
        </div>
        <div id="combo-wrapper" class="hidden">
            <p id="combo-disp">2 COMBO</p>
        </div>
    </div>

    <canvas id="gameCanvas"></canvas>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // 게임 변수
        let gameActive = true;
        let score = 0;
        let combo = 0;
        let maxCombo = 0;
        let shakeIntensity = 0;
        
        let bowPos = { x: 150, y: 0 };
        let currentAngle = 0;
        let shootPower = 28;
        let blinkTimer = 0;
        let arrowTrajectoryVisible = true;
        let isBuffed = false;

        let activeArrows = [];
        let particles = [];
        let scoreTexts = [];
        let envParticles = []; // 날씨/배경 파티클 (구름, 눈, 먼지 등)
        let stars = [];

        // 행성 데이터 및 설정
        const planets = {
            earth: { id: 'earth', gravity: 0.15, name: '지구' },
            moon: { id: 'moon', gravity: 0.05, name: '달' },
            mars: { id: 'mars', gravity: 0.1, name: '화성' },
            venus: { id: 'venus', gravity: 0.13, name: '금성' },
            europa: { id: 'europa', gravity: 0.08, name: '유로파' }
        };
        let currentPlanetKey = 'earth';
        let currentGravity = planets.earth.gravity;

        // 타겟 객체
        let target = {
            x: 0, y: 0,
            radiusD: 80, radiusC: 60, radiusB: 40, radiusA: 20,
            visible: true,
            speed: 2, dir: 1,
            respawnTimer: 0
        };

        // 화살 설정
        let currentArrow = { isApple: false, isGiant: false, width: 95 };

        // 유성(메테오) 이벤트
        let meteor = { active: false, x: 0, y: 0, vx: 0, vy: 0, radius: 40 };

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            bowPos.y = canvas.height / 2;
            target.x = canvas.width - 200;
            if(target.y === 0) target.y = canvas.height / 2;
            initStars();
            initEnvParticles();
        }

        window.addEventListener('resize', resize);

        // 환경 파티클 초기화 (배경 효과용)
        function initEnvParticles() {
            envParticles = [];
            let count = 0;
            if (currentPlanetKey === 'earth') count = 8;       // 구름
            else if (currentPlanetKey === 'mars') count = 40;  // 먼지
            else if (currentPlanetKey === 'venus') count = 60; // 빠른 먼지
            else if (currentPlanetKey === 'europa') count = 100; // 눈

            for (let i = 0; i < count; i++) {
                envParticles.push(createEnvParticle());
            }
        }

        function createEnvParticle() {
            let p = { x: Math.random() * canvas.width, y: Math.random() * canvas.height };
            if (currentPlanetKey === 'earth') {
                p.w = 100 + Math.random() * 150; p.h = 40 + Math.random() * 40;
                p.vx = 0.2 + Math.random() * 0.5; p.vy = 0;
            } else if (currentPlanetKey === 'mars') {
                p.r = 1 + Math.random() * 3;
                p.vx = Math.random() * 0.5 - 0.25; p.vy = Math.random() * 0.5 - 0.25;
            } else if (currentPlanetKey === 'venus') {
                // 오른쪽에서 왼쪽으로 흐르는 먼지
                p.w = 5 + Math.random() * 20; p.h = 2 + Math.random() * 3;
                p.vx = -2 - Math.random() * 4; p.vy = (Math.random() - 0.5) * 0.5;
            } else if (currentPlanetKey === 'europa') {
                // 내리는 눈
                p.r = 1 + Math.random() * 3;
                p.vx = Math.random() * 1 - 0.5; p.vy = 1 + Math.random() * 2;
            }
            return p;
        }

        function initStars() {
            stars = [];
            for(let i=0; i<150; i++) {
                stars.push({ x: Math.random() * canvas.width, y: Math.random() * canvas.height, r: Math.random() * 1.5 });
            }
        }

        function changePlanet(key) {
            currentPlanetKey = key;
            currentGravity = planets[key].gravity;
            
            document.querySelectorAll('.planet-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            initEnvParticles();
            combo = 0;
            document.getElementById('combo-wrapper').classList.add('hidden');
        }

        function shootArrow() {
            if(!gameActive) return;
            let aVx = Math.cos(currentAngle) * shootPower;
            let aVy = Math.sin(currentAngle) * shootPower;
            
            activeArrows.push({
                x: bowPos.x, y: bowPos.y,
                vx: aVx, vy: aVy,
                isApple: currentArrow.isApple,
                isGiant: currentArrow.isGiant,
                width: currentArrow.isGiant ? 240 : 95,
                handled: false
            });

            // 화살 무작위 설정 (사과 화살, 거대 화살 등)
            let rand = Math.random();
            currentArrow.isApple = rand < 0.15;
            currentArrow.isGiant = rand > 0.85;

            // 가끔 메테오 소환
            if(!meteor.active && Math.random() < 0.2) {
                meteor.active = true;
                meteor.x = canvas.width + 100;
                meteor.y = -100;
                meteor.vx = -4 - Math.random()*3;
                meteor.vy = 3 + Math.random()*2;
            }
        }

        // 입력 처리
        window.addEventListener('mousemove', (e) => {
            let dx = e.clientX - bowPos.x;
            let dy = e.clientY - bowPos.y;
            currentAngle = Math.atan2(dy, dx);
            if (currentAngle < -Math.PI/2.5) currentAngle = -Math.PI/2.5;
            if (currentAngle > Math.PI/2.5) currentAngle = Math.PI/2.5;
        });

        window.addEventListener('mousedown', shootArrow);

        // 파티클 생성기
        function createExplosion(x, y, color, count) {
            for(let i=0; i<count; i++) {
                let angle = Math.random() * Math.PI * 2;
                let speed = Math.random() * 5 + 2;
                particles.push({
                    x: x, y: y,
                    vx: Math.cos(angle) * speed, vy: Math.sin(angle) * speed,
                    radius: Math.random() * 4 + 2,
                    color: color, alpha: 1, decay: Math.random() * 0.02 + 0.01
                });
            }
        }

        function createScoreText(x, y, text, color) {
            scoreTexts.push({ x: x, y: y, text: text, color: color, alpha: 1, vy: -1.5 });
        }

        function activateAbilityBuff() {
            isBuffed = true;
            shootPower = 40;
            setTimeout(() => {
                isBuffed = false;
                shootPower = 28;
            }, 5000);
        }

        // 행성별 배경 그리기 (요청하신 구름, 파도, 눈, 갈색 바닥 등)
        function drawDynamicBackground() {
            ctx.save();
            
            // 1. 하늘 색상
            if (currentPlanetKey === 'earth') ctx.fillStyle = '#87CEEB'; // 하늘색
            else if (currentPlanetKey === 'moon') ctx.fillStyle = '#050505'; // 검은색
            else if (currentPlanetKey === 'mars') ctx.fillStyle = '#cda365'; // 뿌연 노란/주황색
            else if (currentPlanetKey === 'venus') ctx.fillStyle = '#dcb858'; // 흐린 진노란색
            else if (currentPlanetKey === 'europa') ctx.fillStyle = '#b0e0e6'; // 뿌연 하늘색
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 달일 경우 별 그리기
            if (currentPlanetKey === 'moon' || currentPlanetKey === 'earth') {
                ctx.fillStyle = "rgba(255,255,255,0.4)";
                stars.forEach(s => {
                    ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill();
                });
            }

            // 2. 파티클 업데이트 및 그리기
            envParticles.forEach(p => {
                p.x += p.vx; p.y += p.vy;
                // 화면 밖으로 나가면 반대편에서 재생성
                if (currentPlanetKey === 'venus' && p.x < -p.w) { p.x = canvas.width + p.w; p.y = Math.random() * canvas.height; }
                else if (p.x > canvas.width + 100) p.x = -100;
                else if (p.x < -100) p.x = canvas.width + 100;
                if (p.y > canvas.height + 10) p.y = -10;

                if (currentPlanetKey === 'earth') {
                    // 구름
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
                    ctx.beginPath(); ctx.ellipse(p.x, p.y, p.w/2, p.h/2, 0, 0, Math.PI*2); ctx.fill();
                    ctx.beginPath(); ctx.arc(p.x - p.w/4, p.y - p.h/3, p.h/1.5, 0, Math.PI*2); ctx.fill();
                    ctx.beginPath(); ctx.arc(p.x + p.w/4, p.y - p.h/4, p.h/1.8, 0, Math.PI*2); ctx.fill();
                } else if (currentPlanetKey === 'mars') {
                    // 화성 먼지
                    ctx.fillStyle = 'rgba(160, 82, 45, 0.5)';
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                } else if (currentPlanetKey === 'venus') {
                    // 금성 모래바람 (가로 선형태)
                    ctx.fillStyle = 'rgba(184, 134, 11, 0.6)';
                    ctx.fillRect(p.x, p.y, p.w, p.h);
                } else if (currentPlanetKey === 'europa') {
                    // 유로파 눈
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                }
            });

            // 3. 바닥 (지형) 그리기
            let groundHeight = 120;
            ctx.beginPath();
            
            if (currentPlanetKey === 'earth') {
                ctx.fillStyle = '#654321'; // 갈색 땅
                ctx.fillRect(0, canvas.height - groundHeight, canvas.width, groundHeight);
                // 잔디 장식
                ctx.fillStyle = '#228b22';
                ctx.fillRect(0, canvas.height - groundHeight, canvas.width, 15);
            } 
            else if (currentPlanetKey === 'moon') {
                ctx.fillStyle = '#444444'; // 울퉁불퉁한 회색 땅
                ctx.moveTo(0, canvas.height - groundHeight);
                for(let i=0; i<=canvas.width; i+=50) {
                    ctx.lineTo(i, canvas.height - groundHeight + Math.sin(i*0.02) * 20);
                }
                ctx.lineTo(canvas.width, canvas.height); ctx.lineTo(0, canvas.height); ctx.fill();
            }
            else if (currentPlanetKey === 'mars') {
                ctx.fillStyle = '#8b4513'; // 갈색 땅
                ctx.moveTo(0, canvas.height - groundHeight);
                for(let i=0; i<=canvas.width; i+=60) {
                    ctx.lineTo(i, canvas.height - groundHeight + Math.cos(i*0.015) * 25);
                }
                ctx.lineTo(canvas.width, canvas.height); ctx.lineTo(0, canvas.height); ctx.fill();
            }
            else if (currentPlanetKey === 'venus') {
                ctx.fillStyle = '#b8860b'; // 진노란색 바닥
                ctx.fillRect(0, canvas.height - groundHeight, canvas.width, groundHeight);
            }
            else if (currentPlanetKey === 'europa') {
                ctx.fillStyle = '#e0ffff'; // 빙판
                ctx.fillRect(0, canvas.height - groundHeight, canvas.width, groundHeight);
                // 금이 간 빙판 표현
                ctx.strokeStyle = '#87cefa'; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(100, canvas.height - groundHeight); ctx.lineTo(150, canvas.height - 40); ctx.lineTo(250, canvas.height - 10); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(400, canvas.height - groundHeight); ctx.lineTo(380, canvas.height - 60); ctx.lineTo(450, canvas.height - 20); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(canvas.width - 200, canvas.height - groundHeight); ctx.lineTo(canvas.width - 150, canvas.height - 50); ctx.stroke();
            }

            ctx.restore();
        }

        // 요청하신 행성 표적 그리기
        function drawPlanetTarget() {
            if(!target.visible) return;
            const skewX = 0.25; 
            
            ctx.save();
            // 기둥 (과녁 거치대 느낌 유지)
            ctx.strokeStyle = "#4a5568"; ctx.lineWidth = 6;
            ctx.beginPath();
            ctx.moveTo(target.x + 5, target.y - target.radiusD); ctx.lineTo(target.x + 5, target.y + target.radiusD);
            ctx.stroke();

            // 그림자
            ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
            ctx.beginPath(); ctx.ellipse(target.x, target.y, (target.radiusD + 6) * skewX, target.radiusD + 6, 0, 0, Math.PI * 2); ctx.fill();

            // 행성 본체 (타원 클리핑)
            ctx.beginPath(); 
            ctx.ellipse(target.x, target.y, target.radiusD * skewX, target.radiusD, 0, 0, Math.PI * 2);
            ctx.save();
            ctx.clip(); // 둥근(타원) 형태 안쪽만 칠해지도록

            if (currentPlanetKey === 'earth') {
                ctx.fillStyle = '#1e90ff'; ctx.fill(); // 파란 바다
                ctx.fillStyle = '#32cd32'; // 초록 육지
                ctx.beginPath(); ctx.arc(target.x - 5, target.y - 30, 25, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(target.x + 10, target.y + 20, 30, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(target.x - 10, target.y + 45, 15, 0, Math.PI*2); ctx.fill();
            } 
            else if (currentPlanetKey === 'moon') {
                ctx.fillStyle = '#aaaaaa'; ctx.fill(); // 회색 바탕
                ctx.fillStyle = '#444444'; // 검은색 자국(크레이터)
                ctx.beginPath(); ctx.arc(target.x - 8, target.y - 20, 12, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(target.x + 5, target.y + 10, 8, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(target.x - 2, target.y + 40, 15, 0, Math.PI*2); ctx.fill();
            }
            else if (currentPlanetKey === 'mars') {
                ctx.fillStyle = '#ff4500'; ctx.fill(); // 주황 바탕
                ctx.fillStyle = '#8b4513'; // 갈색 반점
                ctx.beginPath(); ctx.arc(target.x + 5, target.y - 15, 18, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(target.x - 10, target.y + 25, 20, 0, Math.PI*2); ctx.fill();
            }
            else if (currentPlanetKey === 'venus') {
                ctx.fillStyle = '#ffd700'; ctx.fill(); // 노란 바탕
                ctx.fillStyle = '#daa520'; // 진노란 반점
                ctx.beginPath(); ctx.ellipse(target.x, target.y - 20, 25, 8, Math.PI/6, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.ellipse(target.x, target.y + 20, 20, 10, -Math.PI/4, 0, Math.PI*2); ctx.fill();
            }
            else if (currentPlanetKey === 'europa') {
                ctx.fillStyle = '#f0f8ff'; ctx.fill(); // 청백색 바탕
                ctx.strokeStyle = '#add8e6'; ctx.lineWidth = 3; // 얼음 갈라진 선
                ctx.beginPath(); ctx.moveTo(target.x - 20, target.y - 30); ctx.lineTo(target.x + 20, target.y + 10); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(target.x - 15, target.y + 40); ctx.lineTo(target.x + 10, target.y - 10); ctx.stroke();
            }

            ctx.restore(); // 클리핑 해제
            
            // 행성 테두리
            ctx.strokeStyle = "rgba(255,255,255,0.5)"; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusD * skewX, target.radiusD, 0, 0, Math.PI * 2); ctx.stroke();
            
            ctx.restore();
        }

        // 화살 아이콘 그리기 (제공된 코드 활용)
        function drawArrowIcon(x, y, angle, isApple, isGiant, customWidth) {
            ctx.save();
            ctx.translate(x, y); ctx.rotate(angle);
            let width = customWidth || 95; 
            
            if (isGiant) {
                ctx.strokeStyle = "#ffcc00";
                ctx.lineWidth = 11; 
                ctx.beginPath(); ctx.moveTo(-width/2, 0); ctx.lineTo(width/2, 0); ctx.stroke();

                ctx.fillStyle = "#ff3e3e";
                ctx.beginPath(); ctx.moveTo(width/2, 0); ctx.lineTo(width/2 - 35, -20); ctx.lineTo(width/2 - 35, 20); ctx.closePath(); ctx.fill();

                ctx.fillStyle = "#e3a857";
                ctx.beginPath(); ctx.moveTo(-width/2, 0); ctx.lineTo(-width/2 - 20, -22); ctx.lineTo(-width/2 + 10, -22); ctx.lineTo(-width/2 + 25, 0); ctx.lineTo(-width/2 + 10, 22); ctx.lineTo(-width/2 - 20, 22); ctx.closePath(); ctx.fill();
            } else {
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
            }
            ctx.restore();
        }

        // === 메인 게임 루프 ===
        function update() {
            if (gameActive) {
                // 타겟 상하 이동 로직
                if(target.visible) {
                    target.y += target.speed * target.dir;
                    if(target.y - target.radiusD < 140 || target.y + target.radiusD > canvas.height - 140) {
                        target.dir *= -1; 
                    }
                } else {
                    target.respawnTimer--;
                    if(target.respawnTimer <= 0) {
                        target.y = 180 + Math.random() * (canvas.height - 360);
                        target.visible = true;
                    }
                }

                // 점선 깜빡임
                if(currentArrow.isApple || currentArrow.isGiant) {
                    blinkTimer++;
                    if(blinkTimer % 45 === 0) arrowTrajectoryVisible = !arrowTrajectoryVisible;
                } else {
                    arrowTrajectoryVisible = true;
                }

                // 유성 이동
                if(meteor.active) {
                    meteor.x += meteor.vx;
                    meteor.y += meteor.vy;
                    if(meteor.x < bowPos.x - 20) {
                        meteor.active = false;
                        createExplosion(meteor.x, meteor.y, "#94a3b8", 30);
                        shakeIntensity = 10;
                    }
                }
            }

            // 화면 초기화 및 배경 렌더링
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawDynamicBackground();

            // 화면 흔들림 효과 적용
            ctx.save();
            if (shakeIntensity > 0) {
                ctx.translate((Math.random() - 0.5) * shakeIntensity, (Math.random() - 0.5) * shakeIntensity);
                shakeIntensity *= 0.85; 
                if (shakeIntensity < 0.2) shakeIntensity = 0;
            }

            if(isBuffed && gameActive) {
                ctx.fillStyle = "rgba(255, 62, 62, 0.08)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            // 유성 그리기
            if(meteor.active) {
                ctx.save();
                ctx.fillStyle = "rgba(239, 68, 68, 0.25)";
                ctx.beginPath(); ctx.arc(meteor.x, meteor.y, meteor.radius + 12 + Math.random()*6, 0, Math.PI*2); ctx.fill();

                let grad = ctx.createRadialGradient(meteor.x - 10, meteor.y - 10, 5, meteor.x, meteor.y, meteor.radius);
                grad.addColorStop(0, '#ff9e00'); grad.addColorStop(0.6, '#d946ef'); grad.addColorStop(1, '#450a0a');
                ctx.fillStyle = grad;
                ctx.beginPath(); ctx.arc(meteor.x, meteor.y, meteor.radius, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#ff0055"; ctx.lineWidth = 3; ctx.stroke();
                ctx.restore();
            }

            // 행성 표적 렌더링 (커스텀 함수 호출)
            drawPlanetTarget();

            // 활 그리기 (회전 적용)
            ctx.save();
            ctx.translate(bowPos.x, bowPos.y);
            ctx.rotate(currentAngle);
            
            ctx.strokeStyle = isBuffed ? "#ff0055" : "#00d2ff";
            ctx.lineWidth = 6; 
            ctx.beginPath();
            ctx.arc(-15, 0, 65, -Math.PI/2, Math.PI/2); 
            ctx.stroke();
            
            ctx.strokeStyle = "rgba(255,255,255,0.5)";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(-15, -65); ctx.lineTo(-15, 65);
            ctx.stroke();
            ctx.restore();

            // 대기 중인 화살
            if(gameActive) {
                drawArrowIcon(bowPos.x, bowPos.y, currentAngle, currentArrow.isApple, currentArrow.isGiant, currentArrow.isGiant ? 240 : 95);
            }

            // 조준선(가이드라인) 그리기
            if (arrowTrajectoryVisible && gameActive) {
                let tVx = Math.cos(currentAngle) * shootPower;
                if (tVx > 0) { 
                    ctx.save();
                    if(currentArrow.isGiant) {
                        ctx.strokeStyle = "rgba(255, 204, 0, 0.7)"; ctx.lineWidth = 5;
                    } else {
                        ctx.strokeStyle = currentArrow.isApple ? "#af0404" : "rgba(0, 210, 255, 0.5)"; ctx.lineWidth = 2.5;
                    }
                    ctx.setLineDash([5, 5]);
                    ctx.beginPath();

                    let tX = bowPos.x; let tY = bowPos.y;
                    let tVy = Math.sin(currentAngle) * shootPower;

                    ctx.moveTo(tX, tY);
                    for (let i = 0; i < 60; i++) {
                        tX += tVx; tY += tVy; tVy += currentGravity; 
                        ctx.lineTo(tX, tY);
                        if(tX > canvas.width || tY > canvas.height || tY < 0) break;
                    }
                    ctx.stroke(); ctx.restore();
                }
            }

            const skewX = 0.25; 
            const frontX = target.x - (target.radiusD * skewX); 
            const backX = target.x + (target.radiusD * skewX); 

            // 날아가는 화살 업데이트
            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                
                arrow.x += arrow.vx;
                arrow.y += arrow.vy;
                arrow.vy += currentGravity;

                let arrowAngle = Math.atan2(arrow.vy, arrow.vx);
                drawArrowIcon(arrow.x, arrow.y, arrowAngle, arrow.isApple, arrow.isGiant, arrow.width);

                let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);

                // 화면 밖으로 나감
                if (arrow.x > canvas.width + 150 || arrow.y > canvas.height + 150 || arrow.y < -150) {
                    if(!arrow.handled) {
                        combo = 0; document.getElementById('combo-wrapper').classList.add('hidden');
                    }
                    activeArrows.splice(i, 1);
                    continue;
                }

                // 메테오 타격 판정
                if(meteor.active) {
                    let distToMeteor = Math.hypot(arrowTipX - meteor.x, arrowTipY - meteor.y);
                    if(distToMeteor <= meteor.radius + (arrow.isGiant ? 30 : 10)) {
                        meteor.active = false;
                        activeArrows.splice(i, 1); 
                        createExplosion(meteor.x, meteor.y, "#ffcc00", 50);
                        createScoreText(meteor.x, meteor.y, "AWAKENING!!", "#ffcc00");
                        activateAbilityBuff();
                        continue;
                    }
                }

                // 타겟 명중 판정
                if (target.visible && arrowTipX >= frontX && arrowTipX <= backX + (arrow.isGiant ? 40 : 15) && arrow.vx > 0) {
                    let dy = Math.abs(arrowTipY - target.y);

                    if (dy <= target.radiusD) {
                        arrow.handled = true;
                        target.visible = false;
                        target.respawnTimer = 45; 

                        combo++;
                        if(combo > maxCombo) maxCombo = combo;
                        
                        document.getElementById('combo-disp').innerText = `${combo} COMBO`;
                        document.getElementById('combo-wrapper').classList.remove('hidden');

                        let earnedPoints = 0;
                        let hColor = "#ffffff";
                        
                        // 명중 부위에 따른 점수 계산
                        if (dy <= target.radiusA) { earnedPoints = 10; hColor = "#ffcc00"; }
                        else if (dy <= target.radiusB) { earnedPoints = 5;  hColor = "#ff3e3e"; }
                        else if (dy <= target.radiusC) { earnedPoints = 2;  hColor = "#00d2ff"; }
                        else { earnedPoints = 1;  hColor = "#e2e8f0"; }

                        if(arrow.isApple) { earnedPoints *= 2; hColor = "#ff2222"; }
                        else if(arrow.isGiant) { earnedPoints *= 3; hColor = "#ffcc00"; }

                        let totalEarned = earnedPoints + Math.floor(combo / 3);
                        score += totalEarned;
                        document.getElementById('score-disp').innerText = score;

                        createScoreText(arrowTipX - 25, arrowTipY - 15, `+${totalEarned}`, hColor);
                        
                        shakeIntensity = arrow.isGiant ? 22 : 7; 
                        createExplosion(arrowTipX, arrowTipY, hColor, arrow.isGiant ? 50 : 20);

                        activeArrows.splice(i, 1); 
                        continue;
                    }
                }
            }

            // 폭발 파티클 업데이트
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.x += p.vx; p.y += p.vy; p.alpha -= p.decay;
                if (p.alpha <= 0) { particles.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = p.alpha; ctx.fillStyle = p.color;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI*2); ctx.fill(); ctx.restore();
            }

            // 점수 텍스트 업데이트
            for (let i = scoreTexts.length - 1; i >= 0; i--) {
                let stx = scoreTexts[i];
                stx.y += stx.vy; stx.alpha -= 0.015;
                if(stx.alpha <= 0) { scoreTexts.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = stx.alpha; ctx.fillStyle = stx.color;
                ctx.font = "bold 24px 'Segoe UI'"; ctx.shadowColor = "rgba(0,0,0,0.8)"; ctx.shadowBlur = 4;
                ctx.fillText(stx.text, stx.x, stx.y); ctx.restore();
            }

            ctx.restore(); 
            requestAnimationFrame(update);
        }

        // 초기 실행
        resize();
        update();
    </script>
</body>
</html>
</html>
"""

components.html(game_html, height=720, scrolling=False)
