const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let mouseDown = false;
let lastX, lastY;
let angleX = 0, angleY = 0;
let zoom = 1;

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  render();
});

canvas.addEventListener("mousedown", (e) => {
  mouseDown = true;
  lastX = e.clientX;
  lastY = e.clientY;
});

canvas.addEventListener("mousemove", (e) => {
  if (!mouseDown) return;
  const deltaX = e.clientX - lastX;
  const deltaY = e.clientY - lastY;
  angleX += deltaY * 0.1;
  angleY -= deltaX * 0.1;
  lastX = e.clientX;
  lastY = e.clientY;
  render();
});

canvas.addEventListener("mouseup", () => {
  mouseDown = false;
});

canvas.addEventListener("wheel", (e) => {
  zoom += e.deltaY * -0.01;
  zoom = Math.min(Math.max(zoom, 0.1), 3);
  render();
});

function project(x, y, z) {
  const scale = (zoom * 500) / (500 + z);
  const px = x * scale + canvas.width / 2;
  const py = -y * scale + canvas.height / 2;
  return [px, py];
}

function draw3DShape(vertices, color) {
  const projected = vertices.map((v) => project(v[0], v[1], v[2]));
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(projected[0][0], projected[0][1]);
  for (let i = 1; i < projected.length; i++) {
    ctx.lineTo(projected[i][0], projected[i][1]);
  }
  ctx.closePath();
  ctx.fill();
}

const fuselageVertices = [
  [-75, 0, 0],
  [75, 0, 0],
  [75, 30, 0],
  [-75, 30, 0],
  [-75, 0, -150],
  [75, 0, -150],
  [75, 30, -150],
  [-75, 30, -150],
];

const wingVertices = [
  [-50, 15, 0],
  [50, 15, 0],
  [50, 15, -150],
  [-50, 15, -150],
  [-50, 35, -150],
  [50, 35, -150],
  [50, 35, 0],
  [-50, 35, 0],
];

const tailVertices = [
  [-37.5, 25, -150],
  [37.5, 25, -150],
  [37.5, 65, -150],
  [-37.5, 65, -150],
];

function rotateMatrixX(angle) {
  const cos = Math.cos(angle);
  const sin = Math.sin(angle);
  return [
    [1, 0, 0],
    [0, cos, -sin],
    [0, sin, cos],
  ];
}

function rotateMatrixY(angle) {
  const cos = Math.cos(angle);
  const sin = Math.sin(angle);
  return [
    [cos, 0, sin],
    [0, 1, 0],
    [-sin, 0, cos],
  ];
}

function rotate(vertices, matrix) {
  return vertices.map((v) => [
    v[0] * matrix[0][0] + v[1] * matrix[1][0] + v[2] * matrix[2][0],
    v[0] * matrix[0][1] + v[1] * matrix[1][1] + v[2] * matrix[2][1],
    v[0] * matrix[0][2] + v[1] * matrix[1][2] + v[2] * matrix[2][2],
  ]);
}

function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const rx = rotateMatrixX(angleX);
  const ry = rotateMatrixY(angleY);
  const applyRotation = (verts) => rotate(rotate(verts, rx), ry);
  draw3DShape(applyRotation(fuselageVertices), "gray");
  draw3DShape(applyRotation(wingVertices), "blue");
  draw3DShape(applyRotation(tailVertices), "green");
}

render();
