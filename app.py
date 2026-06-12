import streamlit as st
import streamlit.components.v1 as components

# 페이지 레이아웃 설정
st.set_page_config(page_title="Space Archery Game", layout="centered")
st.title("🏹 우주 양궁 게임 (Space Archery)")
st.write("마우스로 조준하고 클릭해서 화살을 쏘세요! 상단의 행성 버튼을 눌러 환경을 바꿀 수 있습니다.")

# 게임 전체 HTML/JS 소스코드 정의
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Space Archery</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            user-select: none;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            width: 1000px;
            height: 600px;
            margin: 0 auto;
        }
        canvas {
            background: #000;
            display: block;
            border-radius: 12px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            cursor: crosshair;
        }
        #ui-layer {
            position: absolute;
            top: 15px;
            left: 20px;
            right: 20px;
            pointer-events: none;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        .info-box {
            background: rgba(15, 23, 42, 0.65);
            padding: 10px 20px;
            border-radius: 8px;
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255,255,255,0.1);
            font-size: 18px;
            font-weight: bold;
        }
        #combo-wrapper {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid rgba(239, 68, 68, 0.4);
            color: #ef4444;
            transition: all 0.2s;
        }
        .hidden {
            display: none !important;
        }
        #planet-selector {
            position: absolute;
            bottom: 15px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
            background: rgba(15, 23, 42, 0.8);
            padding: 8px 16px;
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .btn {
            background: #334155;
            color: white;
            border: none;
            padding: 6px 14px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.2s;
            pointer-events: auto;
        }
        .btn:hover {
            background: #475569;
        }
        .btn.active {
            background: #0ea5e9;
            box-shadow: 0 0 10px rgba(14, 165, 233, 0.5);
        }
    </style>
</head>
<body>

    <div id="game-container">
        <canvas id="gameCanvas" width="1000" height="600"></canvas>
        
        <div id="ui-layer">
            <div class="info-box">SCORE: <span id="score-disp" style="color: #0ea5e9;">0</span></div>
            <div id="combo-wrapper" class="info-box hidden"><span id="combo-disp">0 COMBO</span></div>
        </div>

        <div id="planet-selector">
            <button class="btn active" onclick="changePlanet('earth')">지구 (Earth)</button>
            <button class="btn" onclick="changePlanet('moon')">달 (Moon)</button>
            <button class="btn" onclick="changePlanet('mars')">화성 (Mars)</button>
            <button class="btn" onclick="changePlanet('venus')">금성 (Venus)</button>
            <button class="btn" onclick="changePlanet('europa')">유로파 (Europa)</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // --- 필수 글로벌 변수 정의부 ---
        let gameActive = true;
        let score = 0;
        let combo = 0;
        let maxCombo = 0;
        let isBuffed = false;
        let buffTimer = 0;
        let blinkTimer = 0;
        let arrowTrajectoryVisible = true;
        let shakeIntensity = 0;
        let gameInterval;

        let mousePos = { x: 0, y: 0 };
        const bowPos = { x: 100, y: 300 };
        let currentAngle = 0;
        let shootPower = 14;

        // 행성 데이터 명세
        const planets = {
            earth: { color: '#2b82c9', gravity: 0.18 },
            moon: { color: '#bbbbbb', gravity: 0.03 },
            mars: { color: '#e03e1d', gravity: 0.07 },
            venus: { color: '#ffd166', gravity: 0.16 },
            europa: { color: '#a5cad6', gravity: 0.04 }
        };
        let currentPlanetKey = 'earth';
        let currentGravity = planets[currentPlanetKey].gravity;

        // 오브젝트 풀 및 상태 배열
        let activeArrows = [];
        let particles = [];
        let scoreTexts = [];
        let stars = [];
        let envParticles = [];

        // 타겟 구조 정의
        let target = {
            x: 820, y: 250,
            radiusA: 12, radiusB: 28, radiusC: 45, radiusD: 60,
            speed: 2.5, dir: 1, visible: true, respawnTimer: 0
        };

        // 메테오 이스터에그 구조 정의
        let meteor = {
            x: 0, y: 0, vx: 0, vy: 0, radius: 22, active: false, destroyed: false, spawnTimer: 200
        };

        let currentArrow = { isApple: false, isGiant: false };

        // --- 초기화 유틸리티 함수 ---
        function initStars() {
            stars = [];
            for (let i = 0; i < 60; i++) {
                stars.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    r: 0.5 + Math.random() * 2
                });
            }
        }

        function initEnvParticles() {
            envParticles = [];
            let count = currentPlanetKey === 'earth' ? 12 : 25;
            for (let i = 0; i < count; i++) {
                envParticles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * (canvas.height - 140),
                    w: 30 + Math.random() * 40,
                    h: 15 + Math.random() * 15,
                    r: 1 + Math.random() * 4,
                    vx: currentPlanetKey === 'venus' ? -(0.5 + Math.random() * 1.5) : (0.2 + Math.random() * 1),
                    vy: currentPlanetKey === 'earth' ? 0 : (Math.random() * 0.2 - 0.1)
                });
            }
        }

        function rollNextArrow() {
            let rand = Math.random();
            if (rand < 0.15) {
                currentArrow = { isApple: true, isGiant: false }; // 애플 화살 (점수 2배)
            } else if (rand > 0.85) {
                currentArrow = { isApple: false, isGiant: true }; // 자이언트 화살 (점수 3배/범위 증가)
            } else {
                currentArrow = { isApple: false, isGiant: false }; // 일반 화살
            }
            blinkTimer = 0;
            arrowTrajectoryVisible = true;
        }

        function spawnMeteor() {
            if (meteor.active) return;
            meteor.x = canvas.width + 50;
            meteor.y = 40 + Math.random() * 150;
            meteor.vx = -(3 + Math.random() * 4);
            meteor.vy = 0.5 + Math.random() * 1.5;
            meteor.active = true;
        }

        function activateAbilityBuff() {
            isBuffed = true;
            buffTimer = 350; // 버프 지속 프레임 수
            shootPower = 20; // 파워 오버차지
        }

        function deactivateAbilityBuff() {
            isBuffed = false;
            shootPower = 14;
        }

        // 행성 스위칭 컨트롤러
        function changePlanet(key) {
            currentPlanetKey = key;
            currentGravity = planets[key].gravity;
            initEnvParticles();
            
            document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
        }

        // 그래픽 자산 가상 렌더러 (UI용 가짜 드로우 호출 방지)
        function drawPlanetButtonsVisual() {}

        // 화살 이미지 리소스 에뮬레이션 그리기 방식
        function drawArrowIcon(x, y, angle, isApple, isGiant, width) {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(angle);

            if (isGiant) {
                ctx.strokeStyle = "#ffcc00"; ctx.lineWidth = 5;
            } else if (isApple) {
                ctx.strokeStyle = "#ff2222"; ctx.lineWidth = 3;
            } else {
                ctx.strokeStyle = "#e2e8f0"; ctx.lineWidth = 2.5;
            }

            // 화살 대
            ctx.beginPath();
            ctx.moveTo(-width / 2, 0);
            ctx.lineTo(width / 2, 0);
            ctx.stroke();

            // 화살 촉
            ctx.fillStyle = ctx.strokeStyle;
            ctx.beginPath();
            ctx.moveTo(width / 2, 0);
            ctx.lineTo(width / 2 - 12, -6);
            ctx.lineTo(width / 2 - 12, 6);
            ctx.fill();

            // 화살 깃초
            ctx.beginPath();
            ctx.moveTo(-width / 2, 0);
            ctx.lineTo(-width / 2 - 8, -8);
            ctx.lineTo(-width / 2 + 4, 0);
            ctx.lineTo(-width / 2 - 8, 8);
            ctx.fill();

            ctx.restore();
        }

        // --- 제공받은 오리지널 게임엔진 소스코드 로직 파트 시작 ---
        
        // (이하 제공하신 마우스 핸들러 및 물리 충돌 판정엔진 완벽 이식)
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

        function getCanvasMousePos(e) {
            const rect = canvas.getBoundingClientRect();
            return {
                x: (e.clientX - rect.left) * (canvas.width / rect.width),
                y: (e.clientY - rect.top) * (canvas.height / rect.height)
            };
        }

        window.addEventListener('mousemove', (e) => {
            mousePos = getCanvasMousePos(e);
            currentAngle = Math.atan2(mousePos.y - bowPos.y, mousePos.x - bowPos.x);
        });

        window.addEventListener('mousedown', (e) => {
            if (!gameActive) return;
            
            let clickedPos = getCanvasMousePos(e);
            if (clickedPos.x >= 0 && clickedPos.x <= canvas.width && clickedPos.y >= 0 && clickedPos.y <= canvas.height) {
                let vx = Math.cos(currentAngle) * shootPower;
                let vy = Math.sin(currentAngle) * shootPower;

                if (vx > 0) {
                    let aWidth = currentArrow.isGiant ? 240 : 95;
                    activeArrows.push({
                        x: bowPos.x, y: bowPos.y,
                        vx: vx, vy: vy,
                        isApple: currentArrow.isApple,
                        isGiant: currentArrow.isGiant,
                        width: aWidth, height: 5,
                        collided: false,
                        handled: false 
                    });
                    rollNextArrow(); 
                }
            }
        });

        drawPlanetButtonsVisual();
        initStars();
        initEnvParticles();
        rollNextArrow();

        function update() {
            // 메테오 자동 스폰 타이머 제어 규칙 추가
            if(gameActive && !meteor.active) {
                meteor.spawnTimer--;
                if(meteor.spawnTimer <= 0) {
                    spawnMeteor();
                    meteor.spawnTimer = 250 + Math.random() * 200;
                }
            }

            if (gameActive && isBuffed) {
                buffTimer--;
                if(buffTimer <= 0) {
                    deactivateAbilityBuff();
                }
            }

            if (gameActive) {
                if(target.visible) {
                    target.y += target.speed * target.dir;
                    if(target.y - target.radiusD < 40 || target.y + target.radiusD > canvas.height - 135) {
                        target.dir *= -1; 
                    }
                } else {
                    target.respawnTimer--;
                    if(target.respawnTimer <= 0) {
                        target.y = 80 + Math.random() * (canvas.height - 240);
                        target.visible = true;
                    }
                }

                if(currentArrow.isApple || currentArrow.isGiant) {
                    blinkTimer++;
                    if(blinkTimer % 45 === 0) {
                        arrowTrajectoryVisible = !arrowTrajectoryVisible;
                    }
                }

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

            ctx.save();
            if (shakeIntensity > 0) {
                ctx.translate((Math.random() - 0.5) * shakeIntensity, (Math.random() - 0.5) * shakeIntensity);
                shakeIntensity *= 0.85; 
                if (shakeIntensity < 0.2) shakeIntensity = 0;
            }

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (currentPlanetKey === 'earth') ctx.fillStyle = '#87CEEB'; 
            else if (currentPlanetKey === 'moon') ctx.fillStyle = '#050505'; 
            else if (currentPlanetKey === 'mars') ctx.fillStyle = '#cda365'; 
            else if (currentPlanetKey === 'venus') ctx.fillStyle = '#dcb858'; 
            else if (currentPlanetKey === 'europa') ctx.fillStyle = '#b0e0e6'; 
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            if (currentPlanetKey === 'moon' || currentPlanetKey === 'earth') {
                ctx.fillStyle = "rgba(255,255,255,0.48)";
                stars.forEach(s => {
                    ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill();
                });
            }

            envParticles.forEach(p => {
                p.x += p.vx; p.y += p.vy;

                if (currentPlanetKey === 'venus' && p.x < -p.w) {
                    p.x = canvas.width + p.w; p.y = Math.random() * (canvas.height - 120);
                } else if (p.x > canvas.width + 120) {
                    p.x = -120; p.y = Math.random() * (canvas.height - 120);
                } else if (p.x < -120) {
                    p.x = canvas.width + 120; p.y = Math.random() * (canvas.height - 120);
                }
                if (p.y > canvas.height - 120) {
                    p.y = -10; p.x = Math.random() * canvas.width;
                }

                if (currentPlanetKey === 'earth') {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.75)';
                    ctx.beginPath(); ctx.ellipse(p.x, p.y, p.w/2, p.h/2, 0, 0, Math.PI*2); ctx.fill();
                    ctx.beginPath(); ctx.arc(p.x - p.w/4, p.y - p.h/3, p.h/1.4, 0, Math.PI*2); ctx.fill();
                    ctx.beginPath(); ctx.arc(p.x + p.w/4, p.y - p.h/4, p.h/1.7, 0, Math.PI*2); ctx.fill();
                } else if (currentPlanetKey === 'mars') {
                    ctx.fillStyle = 'rgba(160, 82, 45, 0.45)';
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                } else if (currentPlanetKey === 'venus') {
                    ctx.fillStyle = 'rgba(150, 105, 15, 0.55)'; 
                    ctx.fillRect(p.x, p.y, p.w, p.h);
                } else if (currentPlanetKey === 'europa') {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.88)'; 
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                }
            });

            if(isBuffed && gameActive) {
                ctx.fillStyle = "rgba(255, 62, 62, 0.05)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            let groundHeight = 120;
            let gY = canvas.height - groundHeight;

            if (currentPlanetKey === 'earth') {
                ctx.fillStyle = '#654321'; 
                ctx.fillRect(0, gY, canvas.width, groundHeight);
                ctx.fillStyle = '#228b22'; 
                ctx.fillRect(0, gY, canvas.width, 16);
            }
            else if (currentPlanetKey === 'moon') {
                ctx.fillStyle = '#444444'; 
                ctx.beginPath();
                ctx.moveTo(0, gY);
                for(let i=0; i<=canvas.width; i+=40) {
                    ctx.lineTo(i, gY + Math.sin(i * 0.025) * 16);
                }
                ctx.lineTo(canvas.width, canvas.height); ctx.lineTo(0, canvas.height); ctx.fill();
            }
            else if (currentPlanetKey === 'mars') {
                ctx.fillStyle = '#8b4513'; 
                ctx.beginPath();
                ctx.moveTo(0, gY);
                for(let i=0; i<=canvas.width; i+=50) {
                    ctx.lineTo(i, gY + Math.cos(i * 0.02) * 22);
                }
                ctx.lineTo(canvas.width, canvas.height); ctx.lineTo(0, canvas.height); ctx.fill();
            }
            else if (currentPlanetKey === 'venus') {
                ctx.fillStyle = '#b8860b'; 
                ctx.fillRect(0, gY, canvas.width, groundHeight);
            }
            else if (currentPlanetKey === 'europa') {
                ctx.fillStyle = '#e0ffff'; 
                ctx.fillRect(0, gY, canvas.width, groundHeight);
                
                ctx.strokeStyle = '#87cefa'; ctx.lineWidth = 3;
                ctx.beginPath(); ctx.moveTo(90, gY); ctx.lineTo(160, canvas.height - 50); ctx.lineTo(240, canvas.height - 15); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(430, gY); ctx.lineTo(390, canvas.height - 40); ctx.lineTo(490, canvas.height - 5); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(850, gY); ctx.lineTo(920, canvas.height - 60); ctx.lineTo(890, canvas.height - 10); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(canvas.width - 150, gY); ctx.lineTo(canvas.width - 90, canvas.height - 45); ctx.stroke();
            }

            const skewX = 0.25; 
            const frontX = target.x - (target.radiusD * skewX); 
            const backX = target.x + (target.radiusD * skewX); 

            if(target.visible) {
                ctx.save();
                ctx.strokeStyle = "rgba(40, 50, 70, 0.5)"; ctx.lineWidth = 5;
                ctx.beginPath(); ctx.moveTo(target.x + 5, target.y - target.radiusD); ctx.lineTo(target.x + 5, target.y + target.radiusD); ctx.stroke();

                ctx.fillStyle = "rgba(0, 0, 0, 0.35)";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, (target.radiusD + 4) * skewX, target.radiusD + 4, 0, 0, Math.PI * 2); ctx.fill();

                ctx.fillStyle = "#ffffff";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusD * skewX, target.radiusD, 0, 0, Math.PI * 2); ctx.fill(); 
                
                ctx.save();
                ctx.beginPath();
                ctx.ellipse(target.x, target.y, target.radiusC * skewX, target.radiusC, 0, 0, Math.PI * 2);
                ctx.clip(); 

                if (currentPlanetKey === 'earth') {
                    ctx.fillStyle = '#2b82c9'; 
                    ctx.fillRect(target.x - 100, target.y - 150, 200, 300);
                    ctx.fillStyle = '#228b22'; 
                    ctx.beginPath();
                    ctx.ellipse(target.x - 10, target.y - 20, 25, 45, Math.PI/6, 0, Math.PI*2);
                    ctx.ellipse(target.x + 20, target.y + 30, 20, 35, -Math.PI/4, 0, Math.PI*2);
                    ctx.ellipse(target.x - 15, target.y + 50, 15, 20, 0, 0, Math.PI*2);
                    ctx.fill();
                } 
                else if (currentPlanetKey === 'moon') {
                    ctx.fillStyle = '#bbbbbb';
                    ctx.fillRect(target.x - 100, target.y - 150, 200, 300);
                    ctx.fillStyle = '#555555'; 
                    ctx.beginPath();
                    ctx.arc(target.x - 12, target.y - 30, 14, 0, Math.PI*2);
                    ctx.arc(target.x + 15, target.y + 10, 18, 0, Math.PI*2);
                    ctx.arc(target.x - 8, target.y + 40, 10, 0, Math.PI*2);
                    ctx.arc(target.x + 8, target.y - 55, 9, 0, Math.PI*2);
                    ctx.fill();
                } 
                else if (currentPlanetKey === 'mars') {
                    ctx.fillStyle = '#e03e1d';
                    ctx.fillRect(target.x - 100, target.y - 150, 200, 300);
                    ctx.fillStyle = '#8b4513';
                    ctx.beginPath();
                    ctx.ellipse(target.x - 15, target.y - 15, 16, 25, Math.PI/3, 0, Math.PI*2);
                    ctx.ellipse(target.x + 18, target.y + 35, 12, 20, -Math.PI/6, 0, Math.PI*2);
                    ctx.arc(target.x - 5, target.y + 55, 11, 0, Math.PI*2);
                    ctx.fill();
                } 
                else if (currentPlanetKey === 'venus') {
                    ctx.fillStyle = '#ffd166';
                    ctx.fillRect(target.x - 100, target.y - 150, 200, 300);
                    ctx.fillStyle = '#b8860b';
                    ctx.beginPath();
                    ctx.ellipse(target.x - 5, target.y - 40, 25, 12, 0, 0, Math.PI*2);
                    ctx.ellipse(target.x + 10, target.y + 15, 22, 10, Math.PI/12, 0, Math.PI*2);
                    ctx.ellipse(target.x - 12, target.y + 45, 18, 9, -Math.PI/8, 0, Math.PI*2);
                    ctx.fill();
                } 
                else if (currentPlanetKey === 'europa') {
                    ctx.fillStyle = '#a5cad6';
                    ctx.fillRect(target.x - 100, target.y - 150, 200, 300);
                    ctx.strokeStyle = '#4682b4'; ctx.lineWidth = 2.5;
                    ctx.beginPath();
                    ctx.moveTo(target.x - 30, target.y - 80); ctx.lineTo(target.x + 30, target.y + 80);
                    ctx.moveTo(target.x + 40, target.y - 50); ctx.lineTo(target.x - 40, target.y + 60);
                    ctx.stroke();
                }
                ctx.restore();

                ctx.fillStyle = "#ff3e3e";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusB * skewX, target.radiusB, 0, 0, Math.PI * 2); ctx.fill();
                
                ctx.fillStyle = "#ffcc00";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusA * skewX, target.radiusA, 0, 0, Math.PI * 2); ctx.fill();
                ctx.restore();
            }

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

            ctx.save();
            ctx.translate(bowPos.x, bowPos.y);
            ctx.rotate(currentAngle);
            
            ctx.strokeStyle = isBuffed ? "#ff0055" : "#00d2ff";
            ctx.lineWidth = 6; 
            ctx.beginPath();
            ctx.arc(-15, 0, 65, -Math.PI/2, Math.PI/2); 
            ctx.stroke();
            
            ctx.strokeStyle = "rgba(255,255,255,0.45)";
            ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(-15, -65); ctx.lineTo(-15, 65); ctx.stroke();
            ctx.restore();

            if(gameActive) {
                drawArrowIcon(bowPos.x, bowPos.y, currentAngle, currentArrow.isApple, currentArrow.isGiant, currentArrow.isGiant ? 240 : 95);
            }

            if (arrowTrajectoryVisible && gameActive) {
                let tVx = Math.cos(currentAngle) * shootPower;
                if (tVx > 0) { 
                    ctx.save();
                    if(currentArrow.isGiant) {
                        ctx.strokeStyle = "rgba(255, 204, 0, 0.75)";
                        ctx.lineWidth = 5.5;
                    } else {
                        ctx.strokeStyle = currentArrow.isApple ? "#ff2222" : "rgba(255, 255, 255, 0.6)";
                        ctx.lineWidth = 2.5;
                    }
                    ctx.setLineDash([6, 6]);
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

            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                
                arrow.x += arrow.vx;
                arrow.y += arrow.vy;
                arrow.vy += currentGravity;

                let arrowAngle = Math.atan2(arrow.vy, arrow.vx);
                drawArrowIcon(arrow.x, arrow.y, arrowAngle, arrow.isApple, arrow.isGiant, arrow.width);

                let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);

                if (arrow.x > canvas.width + 150 || arrow.y > canvas.height + 150 || arrow.y < -150) {
                    if(!arrow.handled) {
                        combo = 0; document.getElementById('combo-wrapper').classList.add('hidden');
                    }
                    activeArrows.splice(i, 1);
                    continue;
                }

                if(meteor.active) {
                    let distToMeteor = Math.hypot(arrowTipX - meteor.x, arrowTipY - meteor.y);
                    if(distToMeteor <= meteor.radius + (arrow.isGiant ? 30 : 10)) {
                        meteor.active = false;
                        meteor.destroyed = true;
                        activeArrows.splice(i, 1); 

                        createExplosion(meteor.x, meteor.y, "#ffcc00", 50);
                        createScoreText(meteor.x, meteor.y, "AWAKENING!!", "#ffcc00");
                        
                        activateAbilityBuff();
                        continue;
                    }
                }

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
                        let targetColor = planets[currentPlanetKey].color;
                        
                        if (dy <= target.radiusA) { earnedPoints = 10; hColor = "#ffcc00"; }
                        else if (dy <= target.radiusB) { earnedPoints = 5;  hColor = "#ff3e3e"; }
                        else if (dy <= target.radiusC) { earnedPoints = 2;  hColor = targetColor; }
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

            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.x += p.vx; p.y += p.vy; p.alpha -= p.decay;
                if (p.alpha <= 0) { particles.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = p.alpha; ctx.fillStyle = p.color;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI*2); ctx.fill(); ctx.restore();
            }

            for (let i = scoreTexts.length - 1; i >= 0; i--) {
                let stx = scoreTexts[i];
                stx.y += stx.vy; stx.alpha -= 0.015;
                if(stx.alpha <= 0) { scoreTexts.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = stx.alpha; ctx.fillStyle = stx.color;
                ctx.font = "bold 22px 'Segoe UI'"; ctx.shadowColor = "rgba(0,0,0,0.5)"; ctx.shadowBlur = 4;
                ctx.fillText(stx.text, stx.x, stx.y); ctx.restore();
            }

            ctx.restore(); 
            if(gameActive) {
                gameInterval = requestAnimationFrame(update);
            } else {
                ctx.clearRect(0,0,canvas.width, canvas.height);
                initStars();
                ctx.fillStyle = "rgba(255,255,255,0.48)";
                stars.forEach(s => { ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill(); });
            }
        }

        // 초기 화면 구성을 위한 1회성 드로우 및 엔진 실행 루프 호출
        initStars();
        ctx.fillStyle = "rgba(255,255,255,0.48)";
        stars.forEach(s => { ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill(); });
        
        // 렌더 루프 최초 작동 호출! (화면이 움직이게 만드는 핵심 코드)
        update();
    </script>
</body>
</html>
"""

# Streamlit 내에 HTML 컴포넌트 렌더링
components.html(game_html, height=640, scrolling=False)
