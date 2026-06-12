import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 레이아웃 설정
st.set_page_config(page_title="우주 양궁 게임", layout="centered")
st.title("🏹 우주 양궁 게임 (Space Archery)")
st.caption("마우스로 조준하고 클릭하여 화살을 쏘세요! 운석을 맞추면 각성 버프가 발동합니다.")

# HTML/CSS/JavaScript 게임 코드 전체 통합
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>우주 양궁 게임</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #111;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 700px;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        #game-container {
            position: relative;
            width: 1000px;
            height: 600px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
            border-radius: 10px;
            overflow: hidden;
        }
        canvas {
            display: block;
            width: 100%;
            height: 100%;
        }
        #ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }
        .score-board {
            position: absolute;
            top: 20px;
            left: 20px;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }
        #combo-wrapper {
            position: absolute;
            top: 60px;
            left: 20px;
            font-size: 20px;
            color: #ffcc00;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            transition: opacity 0.3s;
        }
        .hidden {
            opacity: 0;
        }
        .controls {
            position: absolute;
            bottom: 20px;
            left: 20px;
            pointer-events: auto;
            display: flex;
            gap: 10px;
        }
        button {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.5);
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.2s;
        }
        button:hover {
            background: rgba(255, 255, 255, 0.4);
        }
    </style>
</head>
<body>

    <div id="game-container">
        <canvas id="gameCanvas" width="1000" height="600"></canvas>
        <div id="ui-layer">
            <div class="score-board">SCORE: <span id="score-disp">0</span></div>
            <div id="combo-wrapper" class="hidden"><span id="combo-disp">0 COMBO</span></div>
            
            <div class="controls">
                <button onclick="changePlanet('earth')">지구</button>
                <button onclick="changePlanet('moon')">달</button>
                <button onclick="changePlanet('mars')">화성</button>
                <button onclick="changePlanet('venus')">금성</button>
                <button onclick="changePlanet('europa')">유로파</button>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // --- 전역 변수 초기화 ---
        let gameActive = true; 
        let gameInterval;
        let score = 0;
        let combo = 0;
        let maxCombo = 0;
        
        let mousePos = { x: 0, y: 0 };
        let bowPos = { x: 100, y: canvas.height - 150 };
        let currentAngle = 0;
        let shootPower = 25;
        
        let activeArrows = [];
        let particles = [];
        let scoreTexts = [];
        let stars = [];
        let envParticles = [];
        
        let isBuffed = false;
        let buffTimer = 0;
        let shakeIntensity = 0;
        
        let blinkTimer = 0;
        let arrowTrajectoryVisible = true;
        
        // 행성별 중력 및 색상 테마 설정
        const planets = {
            earth: { gravity: 0.6, color: '#2b82c9' },
            moon: { gravity: 0.15, color: '#bbbbbb' },
            mars: { gravity: 0.35, color: '#e03e1d' },
            venus: { gravity: 0.55, color: '#ffd166' },
            europa: { gravity: 0.25, color: '#a5cad6' }
        };
        let currentPlanetKey = 'earth';
        let currentGravity = planets[currentPlanetKey].gravity;

        // 화살 오브젝트 상태
        let currentArrow = { isApple: false, isGiant: false };

        // 과녁(Target) 설정
        let target = {
            x: canvas.width - 150,
            y: canvas.height / 2,
            radiusD: 60,
            radiusC: 40,
            radiusB: 20,
            radiusA: 10,
            speed: 2.5,
            dir: 1,
            visible: true,
            respawnTimer: 0
        };

        // 이스터에그/이벤트 운석 설정
        let meteor = {
            active: false,
            destroyed: false,
            x: 0, y: 0, vx: 0, vy: 0, radius: 25
        };

        // --- 게임 기능 함수 정의 ---

        function changePlanet(planet) {
            currentPlanetKey = planet;
            currentGravity = planets[planet].gravity;
            initEnvParticles();
        }

        function rollNextArrow() {
            let rand = Math.random();
            currentArrow.isApple = rand < 0.15; // 15% 확률 사과 화살
            currentArrow.isGiant = rand >= 0.15 && rand < 0.25; // 10% 확률 거대 화살
            blinkTimer = 0;
            arrowTrajectoryVisible = true;
        }
        
        function activateAbilityBuff() {
            isBuffed = true;
            buffTimer = 300; // 약 5초 유지
            shootPower = 35; // 발사 속도 상향
        }

        function deactivateAbilityBuff() {
            isBuffed = false;
            shootPower = 25;
        }

        function initStars() {
            stars = [];
            for (let i = 0; i < 150; i++) {
                stars.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    r: Math.random() * 1.5 + 0.5
                });
            }
        }

        function initEnvParticles() {
            envParticles = [];
            for (let i = 0; i < 40; i++) {
                envParticles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() - 0.5) * 2,
                    vy: (Math.random() - 0.5) * 2,
                    w: Math.random() * 15 + 5,
                    h: Math.random() * 10 + 5,
                    r: Math.random() * 4 + 1
                });
            }
        }

        function drawArrowIcon(x, y, angle, isApple, isGiant, length) {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(angle);
            
            // 화살 대
            ctx.strokeStyle = isGiant ? "#ffcc00" : "#ffffff";
            ctx.lineWidth = isGiant ? 6 : 3;
            ctx.beginPath();
            ctx.moveTo(-length/2, 0);
            ctx.lineTo(length/2, 0);
            ctx.stroke();

            // 화살촉
            ctx.fillStyle = isApple ? "#ff2222" : (isGiant ? "#ffaa00" : "#cccccc");
            ctx.beginPath();
            ctx.moveTo(length/2 + 10, 0);
            ctx.lineTo(length/2, -6);
            ctx.lineTo(length/2, 6);
            ctx.fill();

            ctx.restore();
        }

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

        // --- 마우스 이벤트 리스너 리액션 ---
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
                    let aWidth = currentArrow.isGiant ? 160 : 85;
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

        // 엔티티 초기 구동 실행
        rollNextArrow();
        initStars();
        initEnvParticles();

        // --- 메인 애니메이션 루프 (엔진 코어) ---
        function update() {
            if (gameActive && isBuffed) {
                buffTimer--;
                if(buffTimer <= 0) {
                    deactivateAbilityBuff();
                }
            }

            if (gameActive) {
                // 실시간 무작위 운석 출현 연산 (0.5% 확률)
                if (!meteor.active && Math.random() < 0.005) {
                    meteor.active = true;
                    meteor.destroyed = false;
                    meteor.x = canvas.width + 50;
                    meteor.y = Math.random() * (canvas.height / 2);
                    meteor.vx = -3.5 - Math.random() * 2;
                    meteor.vy = 1 + Math.random() * 1.5;
                }

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

            // 스크린 셰이크(진동) 연산 효과
            ctx.save();
            if (shakeIntensity > 0) {
                ctx.translate((Math.random() - 0.5) * shakeIntensity, (Math.random() - 0.5) * shakeIntensity);
                shakeIntensity *= 0.85; 
                if (shakeIntensity < 0.2) shakeIntensity = 0;
            }

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 행성별 고유 하늘 배경색 렌더링
            if (currentPlanetKey === 'earth') ctx.fillStyle = '#87CEEB'; 
            else if (currentPlanetKey === 'moon') ctx.fillStyle = '#050505'; 
            else if (currentPlanetKey === 'mars') ctx.fillStyle = '#cda365'; 
            else if (currentPlanetKey === 'venus') ctx.fillStyle = '#dcb858'; 
            else if (currentPlanetKey === 'europa') ctx.fillStyle = '#111625'; 
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 배경 우주 별무리 드로우
            if (currentPlanetKey === 'moon' || currentPlanetKey === 'earth' || currentPlanetKey === 'europa') {
                ctx.fillStyle = "rgba(255,255,255,0.48)";
                stars.forEach(s => {
                    ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill();
                });
            }

            // 환경 오브젝트(구름, 왜성 대기 파티클) 연산 및 드로우
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
                } else if (currentPlanetKey === 'mars') {
                    ctx.fillStyle = 'rgba(160, 82, 45, 0.45)';
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                } else if (currentPlanetKey === 'venus') {
                    ctx.fillStyle = 'rgba(150, 105, 15, 0.55)'; 
                    ctx.fillRect(p.x, p.y, p.w, p.h);
                } else if (currentPlanetKey === 'europa') {
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)'; 
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                }
            });

            if(isBuffed && gameActive) {
                ctx.fillStyle = "rgba(255, 62, 62, 0.12)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            // 행성별 지형 바닥 표면 처리
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
            }

            // 3D 비스듬한 연출을 위한 입체 과녁 원형 연산 및 드로우
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
                
                ctx.fillStyle = planets[currentPlanetKey].color;
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusC * skewX, target.radiusC, 0, 0, Math.PI * 2); ctx.fill();

                ctx.fillStyle = "#ff3e3e";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusB * skewX, target.radiusB, 0, 0, Math.PI * 2); ctx.fill();
                
                ctx.fillStyle = "#ffcc00";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusA * skewX, target.radiusA, 0, 0, Math.PI * 2); ctx.fill();
                ctx.restore();
            }

            // 운석 그래픽 구현
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

            // 메인 활 장비 컴포넌트 그래픽
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

            // 현재 조준 중인 화살 아이콘 처리
            if(gameActive) {
                drawArrowIcon(bowPos.x, bowPos.y, currentAngle, currentArrow.isApple, currentArrow.isGiant, currentArrow.isGiant ? 150 : 80);
            }

            // 중력 시뮬레이션 기반 예측 가이드 라인(점선) 연산 및 구현
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

            // 공중에 날아가는 투사체 화살 배열 연산
            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                
                arrow.x += arrow.vx;
                arrow.y += arrow.vy;
                arrow.vy += currentGravity; // 실시간 중력 벡터 합산

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

                // 공중 보너스 운석 충돌 처리
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

                // 타겟 과녁 판정 연산 및 충돌 물리 피드백
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

            // 타격 파티클 배열 업데이트 및 페이드아웃 효과
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.x += p.vx; p.y += p.vy; p.alpha -= p.decay;
                if (p.alpha <= 0) { particles.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = p.alpha; ctx.fillStyle = p.color;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI*2); ctx.fill(); ctx.restore();
            }

            // 점수 UI 팝업 텍스트 드로우
            for (let i = scoreTexts.length - 1; i >= 0; i--) {
                let stx = scoreTexts[i];
                stx.y += stx.vy; stx.alpha -= 0.015;
                if(stx.alpha <= 0) { scoreTexts.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = stx.alpha; ctx.fillStyle = stx.color;
                ctx.font = "bold 24px 'Segoe UI'"; ctx.shadowColor = "rgba(0,0,0,0.8)"; ctx.shadowBlur = 4;
                ctx.fillText(stx.text, stx.x, stx.y); ctx.restore();
            }

            ctx.restore(); 

            // 브라우저 프레임 드로우 반복 호출 요청
            if(gameActive) {
                gameInterval = requestAnimationFrame(update);
            }
        }

        // 게임 핵심 루틴 루프 스타트
        update();
    </script>
</body>
</html>
"""

# Streamlit 내에 고유 컴포넌트로 HTML 삽입 및 크기 할당해 출력
components.html(game_html, height=720, scrolling=False)
