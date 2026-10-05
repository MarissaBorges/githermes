document.addEventListener("DOMContentLoaded", () => {
  // 1. Loader Animation (JARVIS Vision Core - Volumetric Plasma)
  const initLoader = () => {
    const canvas = document.getElementById("jarvis-canvas");
    if (!canvas) return;

    canvas.width = 1200;
    canvas.height = 1200;
    const ctx = canvas.getContext("2d");

    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const fov = 1000;
    const cameraZ = 700;
    let time = 0;

    // Helper for 3D Projection
    const project = (x, y, z, rotX, rotY, rotZ) => {
      let x1 = x * Math.cos(rotZ) - y * Math.sin(rotZ);
      let y1 = y * Math.cos(rotZ) + x * Math.sin(rotZ);
      let z1 = z;

      let x2 = x1 * Math.cos(rotY) - z1 * Math.sin(rotY);
      let z2 = z1 * Math.cos(rotY) + x1 * Math.sin(rotY);
      let y2 = y1;

      let y3 = y2 * Math.cos(rotX) - z2 * Math.sin(rotX);
      let z3 = z2 * Math.cos(rotX) + y2 * Math.sin(rotX);
      let x3 = x2;

      const scale = fov / (fov + z3 + cameraZ);
      return {
        x: x3 * scale + centerX,
        y: y3 * scale + centerY,
        z: z3,
        s: scale,
      };
    };

    // --- DATA STRUCTURES ---

    // 0. Topographic Wavy Mesh (A malha de ondas)
    const meshRows = 35;
    const meshCols = 45;
    const meshPoints = [];
    for (let i = 0; i <= meshRows; i++) {
      const lat = Math.PI * (i / meshRows);
      for (let j = 0; j <= meshCols; j++) {
        const lon = 2 * Math.PI * (j / meshCols);
        meshPoints.push({ lat, lon, i, j });
      }
    }

    // 1. Neural Branches (radiating from core to surface)
    const branches = [];
    for (let i = 0; i < 150; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);
      branches.push({
        tx: Math.sin(phi) * Math.cos(theta),
        ty: Math.sin(phi) * Math.sin(theta),
        tz: Math.cos(phi),
        offset: Math.random() * 100,
        thickness: 0.15, // Extremely thin lines
        length: Math.random() * 250 + 150,
      });
    }

    // 2. Surface Arcs (Thick fragmented plasma rings)
    const arcs = [];
    for (let i = 0; i < 50; i++) {
      arcs.push({
        radius: 350 + (Math.random() - 0.5) * 60,
        lat: (Math.random() - 0.5) * Math.PI, // Fixed latitude for this arc
        tiltY: Math.random() * Math.PI, // Random 3D tilt
        tiltZ: Math.random() * Math.PI, // Random 3D tilt
        angle: Math.random() * Math.PI * 2,
        length: Math.random() * Math.PI * 1.2 + 0.2, // arc length
        thickness:
          Math.random() > 0.85
            ? Math.random() * 2 + 1
            : Math.random() * 0.6 + 0.3, // slightly thinner
        speed: (Math.random() - 0.5) * 0.04,
        alpha: Math.random() * 0.7 + 0.2,
      });
    }

    // 3. Particles (Floating glowing dust)
    const particles = [];
    for (let i = 0; i < 200; i++) {
      particles.push({
        theta: Math.random() * Math.PI * 2,
        phi: Math.acos(Math.random() * 2 - 1),
        r: 200 + Math.random() * 200,
        size: Math.random() * 2 + 0.5,
        speed: (Math.random() - 0.5) * 0.03,
      });
    }

    window.meshTickerFn = () => {
      // Clear frame
      ctx.globalCompositeOperation = "source-over";
      ctx.clearRect(0, 0, width, height);

      // Additive blending for true holographic/plasma glow
      ctx.globalCompositeOperation = "lighter";

      const rotX = time * 0.4;
      const rotY = time * 0.6;
      const rotZ = time * 0.2;

      // --- 0. Draw Wavy Topographic Mesh (A Malha Original) ---
      const meshRadius = 380;
      const projectedMesh = [];

      for (let p of meshPoints) {
        const wave1 =
          Math.sin(p.lat * 4 + time) * Math.cos(p.lon * 3 + time * 1.5) * 45;
        const wave2 =
          Math.sin(p.lat * 2 - time * 0.8) * Math.cos(p.lon * 5 - time) * 25;
        const r = meshRadius + wave1 + wave2;

        const stretchX = 1.1;
        const stretchY = 0.7;

        const x = r * Math.sin(p.lat) * Math.cos(p.lon) * stretchX;
        const y = r * Math.cos(p.lat) * stretchY;
        const z = r * Math.sin(p.lat) * Math.sin(p.lon);

        // Add extra mesh tilt
        const proj = project(x, y, z, rotX + Math.PI / 4, rotY, rotZ);
        projectedMesh.push(proj);
      }

      for (let i = 0; i <= meshRows; i++) {
        for (let j = 0; j <= meshCols; j++) {
          const idx = i * (meshCols + 1) + j;
          const p = projectedMesh[idx];
          if (!p) continue;

          const maxZ = meshRadius + 100;
          const minZ = -maxZ;
          let normalizedZ = (p.z - minZ) / (maxZ - minZ);
          normalizedZ = Math.max(0, Math.min(1, normalizedZ));

          // Lower opacity so it blends gracefully with the plasma
          const alpha = Math.pow(1 - normalizedZ, 2.5) * 0.4;
          if (alpha < 0.02) continue;

          ctx.beginPath();
          ctx.strokeStyle = `rgba(251, 191, 36, ${alpha})`;
          ctx.lineWidth = 1;

          if (j < meshCols) {
            const pRight = projectedMesh[idx + 1];
            if (pRight) {
              ctx.moveTo(p.x, p.y);
              ctx.lineTo(pRight.x, pRight.y);
            }
          }

          if (i < meshRows) {
            const pDown = projectedMesh[idx + (meshCols + 1)];
            if (pDown) {
              ctx.moveTo(p.x, p.y);
              ctx.lineTo(pDown.x, pDown.y);
            }
          }
          ctx.stroke();
        }
      }

      // --- 0.5. Draw Equatorial Audio Waves (Voice visualizer) ---
      // These waves are fixed to the mesh's equatorial plane and rotate with it
      const numAudioRings = 4;
      const audioBaseRadius = 450;
      // Colors changed to Yellow/Gold variants
      const ringColors = [
        [251, 191, 36], // Gold
        [255, 220, 50], // Light Yellow
        [255, 180, 0], // Darker Gold
        [255, 240, 100], // Bright Yellow
      ];

      for (let rIdx = 0; rIdx < numAudioRings; rIdx++) {
        ctx.beginPath();
        let first = true;

        // Phase shift based on time for animation
        const phase = time * (4 + rIdx * 0.5) + rIdx * (Math.PI / 2);

        for (let lon = 0; lon <= Math.PI * 2 + 0.1; lon += 0.05) {
          // Sine wave harmonics to simulate voice waveform
          let waveHeight =
            Math.sin(lon * (3 + rIdx) + phase) * 45 +
            Math.cos(lon * (7 - rIdx) - time * 6) * 15;

          // Modulation to make some parts of the wave taller
          const intensity = (Math.sin(lon * 2 + time * 4) + 1) * 0.5;
          waveHeight *= 0.5 + intensity;

          const stretchX = 1.1;
          const x = audioBaseRadius * Math.cos(lon) * stretchX;
          const z = audioBaseRadius * Math.sin(lon);
          const y = waveHeight;

          // Project with exact same rotation as the mesh
          const proj = project(x, y, z, rotX + Math.PI / 4, rotY, rotZ);

          if (first) {
            ctx.moveTo(proj.x, proj.y);
            first = false;
          } else {
            ctx.lineTo(proj.x, proj.y);
          }
        }

        const alpha = 0.6 + rIdx * 0.1;
        const color = ringColors[rIdx % ringColors.length];
        ctx.strokeStyle = `rgba(${color[0]}, ${color[1]}, ${color[2]}, ${alpha})`;
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }

      // --- 1. Draw Volumetric Core ---
      const coreProj = project(0, 0, 0, rotX, rotY, rotZ);
      const coreRadius = 180 * coreProj.s; // Scale with perspective

      // Dynamic core pulsing
      const pulse = Math.sin(time * 5) * 10;

      const grad = ctx.createRadialGradient(
        coreProj.x,
        coreProj.y,
        0,
        coreProj.x,
        coreProj.y,
        coreRadius + pulse,
      );
      grad.addColorStop(0, "rgba(255, 255, 255, 1)"); // White hot center
      grad.addColorStop(0.2, "rgba(255, 220, 50, 0.9)"); // Bright yellow
      grad.addColorStop(0.5, "rgba(255, 100, 0, 0.5)"); // Deep orange
      grad.addColorStop(1, "rgba(255, 50, 0, 0)"); // Fade to invisible

      ctx.beginPath();
      ctx.arc(coreProj.x, coreProj.y, coreRadius + pulse, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      // --- 2. Draw Neural Branches (Imperfect / Jagged / Thin rays) ---
      for (const b of branches) {
        ctx.beginPath();

        const noise = Math.sin(time * 6 + b.offset) * 20;
        const rEnd = b.length + noise;

        const startX = b.tx * 50;
        const startY = b.ty * 50;
        const startZ = b.tz * 50;

        const endX = b.tx * rEnd;
        const endY = b.ty * rEnd;
        const endZ = b.tz * rEnd;

        let pStart = project(startX, startY, startZ, rotX, rotY, rotZ);
        ctx.moveTo(pStart.x, pStart.y);

        const steps = 8;
        for (let j = 1; j <= steps; j++) {
          const t = j / steps;
          let nx = startX + (endX - startX) * t;
          let ny = startY + (endY - startY) * t;
          let nz = startZ + (endZ - startZ) * t;

          // Add jagged noise for imperfection
          if (j < steps) {
            const jitter = 30; // amount of zig-zag
            nx += (Math.random() - 0.5) * jitter;
            ny += (Math.random() - 0.5) * jitter;
            nz += (Math.random() - 0.5) * jitter;
          }

          const pNext = project(nx, ny, nz, rotX, rotY, rotZ);
          ctx.lineTo(pNext.x, pNext.y);
        }

        ctx.strokeStyle = `rgba(255, 140, 0, 0.6)`;
        ctx.lineWidth = b.thickness * pStart.s;
        ctx.lineJoin = "miter";
        ctx.stroke();
      }

      // --- 3. Draw Fragmented Surface Arcs (Liquid / Imperfect structures) ---
      for (const arc of arcs) {
        ctx.beginPath();
        arc.angle += arc.speed;

        let first = true;
        for (let lon = arc.angle; lon <= arc.angle + arc.length; lon += 0.08) {
          // Base coordinates using fixed latitude
          let bx = arc.radius * Math.sin(arc.lat) * Math.cos(lon);
          let by = arc.radius * Math.cos(arc.lat);
          let bz = arc.radius * Math.sin(arc.lat) * Math.sin(lon);

          // Add noise for liquid/imperfect look
          const noise = Math.sin(lon * 15 + time * 3) * 8;
          bx += noise;
          by += noise;
          bz += noise;

          // Apply 3D tilt specific to this arc
          let tx = bx * Math.cos(arc.tiltZ) - by * Math.sin(arc.tiltZ);
          let ty = by * Math.cos(arc.tiltZ) + bx * Math.sin(arc.tiltZ);
          let tz = bz;

          let fx = tx * Math.cos(arc.tiltY) - tz * Math.sin(arc.tiltY);
          let fz = tz * Math.cos(arc.tiltY) + tx * Math.sin(arc.tiltY);
          let fy = ty;

          const proj = project(fx, fy, fz, rotX, rotY, rotZ);

          if (first) {
            ctx.moveTo(proj.x, proj.y);
            first = false;
          } else ctx.lineTo(proj.x, proj.y);
        }

        // Random flickering
        const flicker = Math.random() > 0.95 ? 0.1 : arc.alpha;
        ctx.strokeStyle = `rgba(255, 180, 0, ${flicker})`;
        ctx.lineWidth = arc.thickness;
        ctx.stroke();
      }

      // --- 4. Draw Particles ---
      for (const p of particles) {
        p.theta += p.speed;

        const x = p.r * Math.sin(p.phi) * Math.cos(p.theta);
        const y = p.r * Math.cos(p.phi);
        const z = p.r * Math.sin(p.phi) * Math.sin(p.theta);

        const proj = project(x, y, z, rotX, rotY, rotZ);

        ctx.beginPath();
        ctx.arc(proj.x, proj.y, p.size * proj.s, 0, Math.PI * 2);
        // Glowing bright yellow/white particles
        ctx.fillStyle = `rgba(255, 230, 100, ${Math.random() * 0.6 + 0.4})`;
        ctx.fill();
      }

      time += 0.025;
    };

    gsap.ticker.add(window.meshTickerFn);
  };

  // 2. Transition Loader to Floating Chat Button after 5.5 seconds
  const hideLoader = () => {
    // Fade out background and text
    gsap.to(["#loader-bg", "#loader-text"], {
      opacity: 0,
      duration: 1,
      delay: 5.5,
      onComplete: () => {
        const bg = document.getElementById("loader-bg");
        if (bg) bg.style.display = "none";
        const txt = document.getElementById("loader-text");
        if (txt) txt.style.display = "none";
        
        // Unblock the screen
        const wrapper = document.getElementById("loader-wrapper");
        if (wrapper) wrapper.classList.remove("fixed", "inset-0", "z-[100]");
        
        showToast("System mesh loaded successfully", "success");
        animateViewIn("#view-overview");
      },
    });

    // Animate the orb container to the bottom right
    setTimeout(() => {
      const orb = document.getElementById("orb-container");
      if (!orb) return;
      
      const rect = orb.getBoundingClientRect();
      
      // Lock its current position from the Flexbox layout
      orb.style.position = "fixed";
      orb.style.left = rect.left + "px";
      orb.style.top = rect.top + "px";
      orb.style.width = rect.width + "px";
      orb.style.height = rect.height + "px";
      orb.style.maxWidth = "none";
      
      // Reduce the intense ambient glow
      gsap.to("#orb-glow", { opacity: 0.1, duration: 1.5 });

      // Animate from its exact center position to the bottom right
      gsap.to(orb, {
        duration: 1.5,
        ease: "power3.inOut",
        left: window.innerWidth - 132, // 100px width + 32px right padding
        top: window.innerHeight - 132, // 100px height + 32px bottom padding
        width: 100,
        height: 100,
        onComplete: () => {
          orb.style.left = "auto";
          orb.style.top = "auto";
          orb.style.right = "32px";
          orb.style.bottom = "32px";
          orb.style.zIndex = "95";
          orb.classList.add("shadow-[0_0_30px_rgba(251,191,36,0.15)]", "rounded-full");
        }
      });
    }, 5500);
  };

  // 3. View Management
  const views = ["#view-overview", "#view-chat", "#view-repos"];

  const animateViewOut = (viewId, callback) => {
    gsap.to(`${viewId} > *`, {
      y: -20,
      opacity: 0,
      duration: 0.4,
      stagger: 0.05,
      ease: "power2.in",
      onComplete: () => {
        document.querySelector(viewId).classList.add("hidden");
        if (callback) callback();
      },
    });
  };

  const animateViewIn = (viewId) => {
    document.querySelector(viewId).classList.remove("hidden");
    gsap.fromTo(
      `${viewId} > *`,
      { y: 20, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.5, stagger: 0.1, ease: "power3.out" },
    );
  };

  window.switchView = (targetViewId) => {
    const currentViewId = views.find(
      (v) => !document.querySelector(v).classList.contains("hidden"),
    );
    if (currentViewId === targetViewId) return;

    if (currentViewId) {
      animateViewOut(currentViewId, () => {
        animateViewIn(targetViewId);
      });
    } else {
      animateViewIn(targetViewId);
    }

    // Update nav active states
    document.querySelectorAll("nav a").forEach((a) => {
      a.classList.remove("bg-surface", "text-primary");
      a.classList.add("text-secondary");
    });
    const targetNav = document.querySelector(`[data-target="${targetViewId}"]`);
    if (targetNav) {
      targetNav.classList.remove("text-secondary");
      targetNav.classList.add("bg-surface", "text-primary");
    }
  };

  // 4. Toast System
  window.showToast = (message, type = "info") => {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");

    let icon = "ph-info";
    let color = "text-primary";
    if (type === "success") {
      icon = "ph-check-circle";
      color = "text-gold";
    }
    if (type === "error") {
      icon = "ph-warning-circle";
      color = "text-red-500";
    }

    toast.className = `toast flex items-center gap-3 bg-surface border border-border px-4 py-3 rounded-lg shadow-lg mb-3 transform-gpu`;
    toast.innerHTML = `
            <i class="ph ${icon} ${color} text-lg"></i>
            <span class="text-sm font-medium text-primary">${message}</span>
        `;

    container.appendChild(toast);

    // Animate in
    gsap.fromTo(
      toast,
      { x: 100, opacity: 0 },
      { x: 0, opacity: 1, duration: 0.4, ease: "back.out(1.5)" },
    );

    // Animate out after 4 seconds
    setTimeout(() => {
      gsap.to(toast, {
        x: 100,
        opacity: 0,
        duration: 0.4,
        ease: "power2.in",
        onComplete: () => toast.remove(),
      });
    }, 4000);
  };

  // Initialize
  initLoader();
  hideLoader();

  // Event listeners for Navigation
  document.querySelectorAll("[data-target]").forEach((el) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      switchView(el.getAttribute("data-target"));
    });
  });
});
