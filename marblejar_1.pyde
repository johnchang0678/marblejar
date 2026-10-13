<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Interactive Marble Jar</title>
    <style>
        body {
            margin: 0;
            background-color: #E8F1F5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: Arial, sans-serif;
        }
        canvas {
            background-color: #E8F1F5;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.15);
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <canvas id="marbleCanvas" width="1400" height="800"></canvas>
    
    <script>
        var canvas = document.getElementById('marbleCanvas');
        var ctx = canvas.getContext('2d');

        // --- Layout Configuration ---
        var CANVAS_WIDTH = 1400;
        var CANVAS_HEIGHT = 800;
        var JAR_WIDTH = 450;
        var JAR_HEIGHT = 480;
        var JAR_X = (CANVAS_WIDTH - JAR_WIDTH) / 2;
        var JAR_Y = 160;

        var MARBLE_SIZE = 24;
        var SPACING = 26;
        var COLS = Math.floor((JAR_WIDTH - 30) / SPACING);

        var marbles = [];
        var COLORS = ["#D9534F", "#337AB7", "#5CB85C", "#F0AD4E", "#8E44AD", "#34495E", "#E67E22"];

        // --- Safe Persistent Storage ---
        function loadMarbles() {
            var count = 28;
            try {
                var saved = localStorage.getItem("github_marble_jar_count");
                if (saved !== null && saved !== undefined) {
                    var parsed = parseInt(saved, 10);
                    if (!isNaN(parsed) && parsed >= 0 && parsed <= 150) {
                        count = parsed;
                    }
                }
            } catch (e) {
                // Fallback to default if storage is restricted
                count = 28;
            }

            for (var i = 0; i < count; i++) {
                addMarbleToGrid(i);
            }
        }

        function saveMarbles() {
            try {
                localStorage.setItem("github_marble_jar_count", marbles.length);
            } catch (e) {
                // Ignore storage errors if blocked
            }
        }

        // --- Bottom-Up Grid Stacking Logic ---
        function addMarbleToGrid(index) {
            var col = index % COLS;
            var row = Math.floor(index / COLS);
            
            var x = JAR_X + 20 + (col * SPACING) + (MARBLE_SIZE / 2);
            var y = (JAR_Y + JAR_HEIGHT - 15) - (row * SPACING) - (MARBLE_SIZE / 2);
            
            var color = COLORS[index % COLORS.length];
            marbles.push({ x: x, y: y, color: color });
        }

        function addMarbles(amount) {
            for (var i = 0; i < amount; i++) {
                if (marbles.length < 150) {
                    addMarbleToGrid(marbles.length);
                }
            }
            saveMarbles();
            draw();
        }

        function removeMarbles(amount) {
            for (var i = 0; i < amount; i++) {
                if (marbles.length > 0) {
                    marbles.pop();
                }
            }
            saveMarbles();
            draw();
        }

        // --- Render Function ---
        function draw() {
            ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

            // 1. Main Header Title
            ctx.fillStyle = "#2C3E50";
            ctx.font = "bold 28px Arial";
            ctx.textAlign = "center";
            ctx.fillText("MARBLES IN JAR: " + marbles.length + " / 150", CANVAS_WIDTH / 2, 50);

            // 2. Class Sub-Header
            ctx.font = "18px Arial";
            ctx.fillStyle = "#646E7D";
            ctx.fillText("class", CANVAS_WIDTH / 2, 88);

            // 3. Draw Glass Jar Walls
            ctx.strokeStyle = "#333333";
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(JAR_X, JAR_Y);
            ctx.lineTo(JAR_X, JAR_Y + JAR_HEIGHT);
            ctx.lineTo(JAR_X + JAR_WIDTH, JAR_Y + JAR_HEIGHT);
            ctx.lineTo(JAR_X + JAR_WIDTH, JAR_Y);
            ctx.stroke();

            // 4. Jar Top Rim Lip
            ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
            ctx.lineWidth = 4;
            ctx.fillRect(JAR_X - 20, JAR_Y - 20, JAR_WIDTH + 40, 20);
            ctx.strokeRect(JAR_X - 20, JAR_Y - 20, JAR_WIDTH + 40, 20);

            // 5. Draw Marbles Inside (with Black Borders)
            for (var i = 0; i < marbles.length; i++) {
                var m = marbles[i];
                ctx.fillStyle = m.color;
                ctx.strokeStyle = "#000000";
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.arc(m.x, m.y, MARBLE_SIZE / 2, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();
            }

            // 6. Draw Control Buttons
            var btnY = 690;
            var btnW = 110;
            var btnH = 60;
            var bulkW = 100;

            // --- LEFT SIDE: Minus Controls ---
            // [-10] Button
            ctx.fillStyle = "#C0392B";
            ctx.fillRect(CANVAS_WIDTH / 2 - 370, btnY, bulkW, btnH);
            ctx.fillStyle = "#FFFFFF";
            ctx.font = "bold 20px Arial";
            ctx.fillText("-10", CANVAS_WIDTH / 2 - 320, btnY + 35);

            // [- REMOVE] Button
            ctx.fillStyle = "#E74C3C";
            ctx.fillRect(CANVAS_WIDTH / 2 - 255, btnY, btnW, btnH);
            ctx.fillStyle = "#FFFFFF";
            ctx.fillText("- REMOVE", CANVAS_WIDTH / 2 - 200, btnY + 35);

            // --- RIGHT SIDE: Add Controls ---
            // [+ ADD] Button
            ctx.fillStyle = "#2ECC71";
            ctx.fillRect(CANVAS_WIDTH / 2 + 145, btnY, btnW, btnH);
            ctx.fillStyle = "#FFFFFF";
            ctx.fillText("+ ADD", CANVAS_WIDTH / 2 + 200, btnY + 35);

            // [+10] Button
            ctx.fillStyle = "#27AE60";
            ctx.fillRect(CANVAS_WIDTH / 2 + 270, btnY, bulkW, btnH);
            ctx.fillStyle = "#FFFFFF";
            ctx.fillText("+10", CANVAS_WIDTH / 2 + 320, btnY + 35);

            // 7. Footer Instructions
            ctx.fillStyle = "#555555";
            ctx.font = "14px Arial";
            ctx.fillText("Click screen buttons or use [UP] / [DOWN] arrow keys.", CANVAS_WIDTH / 2, 770);
        }

        // --- Mouse Click Listeners ---
        canvas.addEventListener('click', function(e) {
            var rect = canvas.getBoundingClientRect();
            var scaleX = canvas.width / rect.width;
            var scaleY = canvas.height / rect.height;
            var mouseX = (e.clientX - rect.left) * scaleX;
            var mouseY = (e.clientY - rect.top) * scaleY;

            var btnY = 690;
            // Check [-10] Click (Left)
            if (mouseX >= CANVAS_WIDTH / 2 - 370 && mouseX <= CANVAS_WIDTH / 2 - 270 && mouseY >= btnY && mouseY <= btnY + 60) {
                removeMarbles(10);
            }
            // Check [- REMOVE] Click (Left)
            else if (mouseX >= CANVAS_WIDTH / 2 - 255 && mouseX <= CANVAS_WIDTH / 2 - 145 && mouseY >= btnY && mouseY <= btnY + 60) {
                removeMarbles(1);
            }
            // Check [+ ADD] Click (Right)
            else if (mouseX >= CANVAS_WIDTH / 2 + 145 && mouseX <= CANVAS_WIDTH / 2 + 255 && mouseY >= btnY && mouseY <= btnY + 60) {
                addMarbles(1);
            }
            // Check [+10] Click (Right)
            else if (mouseX >= CANVAS_WIDTH / 2 + 270 && mouseX <= CANVAS_WIDTH / 2 + 370 && mouseY >= btnY && mouseY <= btnY + 60) {
                addMarbles(10);
            }
        });

        // --- Keyboard Shortcut Listeners ---
        window.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowUp' || e.key === '+' || e.key === '=') {
                addMarbles(1);
            } else if (e.key === 'ArrowDown' || e.key === '-' || e.key === '_') {
                removeMarbles(1);
            }
        });

        // --- Initialize Application ---
        loadMarbles();
        draw();
    </script>
</body>
</html>
