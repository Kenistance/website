import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

const CompletedProjectPrism = () => {
  const containerRef = useRef();
  const [hovered, setHovered] = useState(false);

  useEffect(() => {
    if (!containerRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      45,
      containerRef.current.clientWidth / containerRef.current.clientHeight,
      0.1,
      1000
    );
    camera.position.z = 30;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight);
    containerRef.current.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 10);
    scene.add(directionalLight);

    // Create octagonal prism geometry
    const radius = 5;
    const height = 8;
    const sides = 8;
    const shape = new THREE.Shape();
    for (let i = 0; i < sides; i++) {
      const theta = (i / sides) * Math.PI * 2;
      const x = radius * Math.cos(theta);
      const y = radius * Math.sin(theta);
      if (i === 0) shape.moveTo(x, y);
      else shape.lineTo(x, y);
    }
    shape.closePath();

    const extrudeSettings = { depth: height, bevelEnabled: false };
    const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);

    // Create texture for text on prism face
    const createTextTexture = (textLines, width = 512, height = 512) => {
      const canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext('2d');

      // Background transparent
      ctx.clearRect(0, 0, width, height);

      // Text styling
      ctx.fillStyle = hovered ? '#FF6F61' : '#00FFFF'; // appetizing color on hover, cyan otherwise
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      ctx.font = 'bold 36px Arial';
      ctx.shadowColor = 'rgba(0,0,0,0.7)';
      ctx.shadowBlur = 4;

      // Draw multiple lines vertically centered
      const lineHeight = 48;
      const totalHeight = textLines.length * lineHeight;
      let startY = height / 2 - totalHeight / 2 + lineHeight / 2;

      textLines.forEach((line, i) => {
        ctx.fillText(line, width / 2, startY + i * lineHeight);
      });

      const texture = new THREE.CanvasTexture(canvas);
      texture.needsUpdate = true;
      return texture;
    };

    // Updated text lines for prism face with "Completed Projects"
    const textLines = [
      "Completed Projects",
      "Farmconnect",
      "",
      "A website connecting farmers",
      "with real-time information.",
      "Price trends, demand & supply,",
      "top-selling product trends,",
      "and more insights."
    ];

    // Create materials: one for each face of the prism
    const materials = [];

    // We'll create one face material with text texture for the front face
    // and a neutral material for the rest
    const textTexture = createTextTexture(textLines);

    for (let i = 0; i < geometry.groups.length; i++) {
      // group 0 is sides, group 1 is front face, group 2 is back face
      if (i === 1) {
        materials.push(new THREE.MeshPhongMaterial({ map: textTexture, transparent: true }));
      } else {
        materials.push(
          new THREE.MeshPhongMaterial({
            color: hovered ? 0xFF6F61 : 0x00FFFF,
            opacity: 0.85,
            transparent: true,
            shininess: 100,
            side: THREE.DoubleSide,
          })
        );
      }
    }

    const prism = new THREE.Mesh(geometry, materials);
    prism.rotation.x = Math.PI / 8; // slight tilt for cool effect
    prism.rotation.y = 0;
    prism.position.z = -height / 2;
    scene.add(prism);

    // Animation parameters for bouncing zigzag
    let clock = new THREE.Clock();
    const amplitudeX = 12;
    const amplitudeY = 4;
    const speed = 1; // controls speed of bounce

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);

      const elapsed = clock.getElapsedTime();

      // Zigzag bouncing motion left-right with sinusoidal Y offset
      prism.position.x = amplitudeX * Math.sin(speed * elapsed);
      prism.position.y = amplitudeY * Math.sin(speed * elapsed * 3); // faster Y bounce for zigzag
      prism.rotation.y += 0.01;

      renderer.render(scene, camera);
    };

    animate();

    // Handle resizing
    const handleResize = () => {
      if (!containerRef.current) return;
      const width = containerRef.current.clientWidth;
      const height = containerRef.current.clientHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };

    window.addEventListener('resize', handleResize);

    // Cleanup on unmount
    return () => {
      window.removeEventListener('resize', handleResize);
      if (containerRef.current && renderer.domElement && containerRef.current.contains(renderer.domElement)) {
        containerRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, [hovered]);

  // Mouse event handlers to toggle hovered state for color change
  const onPointerOver = () => setHovered(true);
  const onPointerOut = () => setHovered(false);

  return (
    <div
      ref={containerRef}
      style={{ width: '100%', height: '400px', cursor: 'pointer', margin: '2rem 0' }}
      onPointerOver={onPointerOver}
      onPointerOut={onPointerOut}
    />
  );
};

export default CompletedProjectPrism;
