const fs = require('fs');

const inputData = JSON.parse(fs.readFileSync('/dev/stdin', 'utf8'));
const mapSize = inputData.map_size;
const warehouseX = mapSize[0] / 2;
const warehouseY = mapSize[1] / 2;
const drones = inputData.drones;
const deliveries = inputData.deliveries;
const noFlyZones = inputData.no_fly_zones || [];
const chargingStations = inputData.charging_stations || [];

const BATTERY_CAP = 500;
const CHARGE_RATE = 2;
const EPS = 1e-9;

function dist(x1, y1, x2, y2) {
  return Math.sqrt((x2-x1)**2 + (y2-y1)**2);
}

function segmentCircleInterval(ax, ay, bx, by, cx, cy, r) {
  const dx = bx - ax;
  const dy = by - ay;
  const fx = ax - cx;
  const fy = ay - cy;
  const A = dx*dx + dy*dy;
  if (A < EPS) {
    const dist2 = fx*fx + fy*fy;
    if (dist2 <= r*r) return [0, 0];
    return null;
  }
  const B = 2*(fx*dx + fy*dy);
  const C = fx*fx + fy*fy - r*r;
  const disc = B*B - 4*A*C;
  if (disc < 0) return null;
  const sqrtDisc = Math.sqrt(Math.max(0, disc));
  const t1 = (-B - sqrtDisc) / (2*A);
  const t2 = (-B + sqrtDisc) / (2*A);
  const tEnter = Math.min(t1, t2);
  const tExit = Math.max(t1, t2);
  const t0 = Math.max(0, tEnter);
  const t1c = Math.min(1, tExit);
  if (t0 > t1c) return null;
  const len = Math.sqrt(A);
  return [t0 * len, t1c * len];
}

function segmentRectInterval(ax, ay, bx, by, xmin, ymin, xmax, ymax) {
  const dx = bx - ax;
  const dy = by - ay;
  let t0 = 0, t1 = 1;
  const clip = (p, q) => {
    if (Math.abs(p) < EPS) return q >= 0;
    const r = q / p;
    if (p < 0) { if (r > t1) return false; if (r > t0) t0 = r; }
    else { if (r < t0) return false; if (r < t1) t1 = r; }
    return true;
  };
  if (!clip(-dx, ax - xmin)) return null;
  if (!clip(dx, xmax - ax)) return null;
  if (!clip(-dy, ay - ymin)) return null;
  if (!clip(dy, ymax - ay)) return null;
  if (t0 > t1) return null;
  const len = dist(ax, ay, bx, by);
  return [t0 * len, t1 * len];
}

function nfzSegmentInterval(ax, ay, bx, by, nfz) {
  if (nfz.shape === 'circle') {
    return segmentCircleInterval(ax, ay, bx, by, nfz.center[0], nfz.center[1], nfz.radius);
  }
  const [[xmin, ymin], [xmax, ymax]] = nfz.corners;
  return segmentRectInterval(ax, ay, bx, by, Math.min(xmin, xmax), Math.min(ymin, ymax), Math.max(xmin, xmax), Math.max(ymin, ymax));
}

function earliestSafeStart(ax, ay, bx, by, t0) {
  let start = t0;
  let changed = true;
  let guard = 0;
  while (changed && guard < 1000) {
    changed = false;
    guard++;
    for (const nfz of noFlyZones) {
      const interval = nfzSegmentInterval(ax, ay, bx, by, nfz);
      if (!interval) continue;
      const [sEnter] = interval;
      const [sE, sX] = interval;
      const enterTime = start + sE;
      const exitTime = start + sX;
      if (enterTime <= nfz.T_end + EPS && exitTime >= nfz.T_start - EPS) {
        const newStart = nfz.T_end - sEnter + 1e-6;
        if (newStart > start + EPS) {
          start = newStart;
          changed = true;
        }
      }
    }
  }
  return start;
}

function addLeg(path, ax, ay, bx, by, payload, timeRef, batteryRef) {
  let start = earliestSafeStart(ax, ay, bx, by, timeRef.t);
  if (start > timeRef.t + EPS) {
    path.push({ x: ax, y: ay, t: start, action: 'WAIT' });
    timeRef.t = start;
  }
  const d = dist(ax, ay, bx, by);
  const energy = d * (1 + payload);
  if (batteryRef.b + EPS < energy) return false;
  batteryRef.b -= energy;
  timeRef.t += d;
  return true;
}

function simulateTrip(deliveryList, startT) {
  if (!deliveryList.length) return null;
  const path = [];
  let payload = deliveryList.reduce((s, d) => s + d.weight, 0);
  let cx = warehouseX, cy = warehouseY;
  const timeRef = { t: startT };
  const batteryRef = { b: BATTERY_CAP };

  path.push({ x: warehouseX, y: warehouseY, t: startT, action: 'PICKUP', delivery_ids: deliveryList.map(d => d.id) });

  for (const d of deliveryList) {
    if (!addLeg(path, cx, cy, d.x, d.y, payload, timeRef, batteryRef)) return null;
    cx = d.x; cy = d.y;
    path.push({ x: d.x, y: d.y, t: timeRef.t, action: 'DELIVER', delivery_id: d.id });
    if (timeRef.t > d.deadline + EPS) return null;
    payload -= d.weight;
  }

  const needReturn = dist(cx, cy, warehouseX, warehouseY) * (1 + payload);
  if (batteryRef.b + EPS < needReturn) {
    if (!chargingStations.length) return null;
    let best = null, bestDist = Infinity;
    for (const cs of chargingStations) {
      const d = dist(cx, cy, cs.x, cs.y);
      if (d < bestDist) { bestDist = d; best = cs; }
    }
    if (!addLeg(path, cx, cy, best.x, best.y, payload, timeRef, batteryRef)) return null;
    cx = best.x; cy = best.y;
    path.push({ x: cx, y: cy, t: timeRef.t, action: 'CHARGE' });
    const need = dist(cx, cy, warehouseX, warehouseY);
    if (batteryRef.b + EPS < need) {
      const deficit = need - batteryRef.b;
      const chargeTime = Math.ceil(deficit / CHARGE_RATE);
      timeRef.t += chargeTime;
      batteryRef.b += chargeTime * CHARGE_RATE;
      path.push({ x: cx, y: cy, t: timeRef.t, action: 'CHARGE_COMPLETE' });
    }
  }

  if (!addLeg(path, cx, cy, warehouseX, warehouseY, payload, timeRef, batteryRef)) return null;
  path.push({ x: warehouseX, y: warehouseY, t: timeRef.t, action: 'RETURN' });
  return { path, endTime: timeRef.t };
}

function pickBestSingle(deliveryList, startT, maxPayload) {
  let best = null;
  let bestEnd = Infinity;
  for (const d of deliveryList) {
    if (d.weight > maxPayload + EPS) continue;
    const trip = simulateTrip([d], startT);
    if (!trip) continue;
    if (trip.endTime < bestEnd) {
      bestEnd = trip.endTime;
      best = d;
    }
  }
  return best;
}

const flightManifest = [];
const remaining = [...deliveries];

const droneStates = drones.map(d => ({ drone: d, t: 0, path: [] }));

let progress = true;
while (progress && remaining.length) {
  progress = false;
  for (const state of droneStates) {
    const pick = pickBestSingle(remaining, state.t, state.drone.max_payload);
    if (!pick) continue;
    const trip = simulateTrip([pick], state.t);
    if (!trip) continue;
    state.path.push(...trip.path);
    state.t = trip.endTime;
    const idx = remaining.findIndex(d => d.id === pick.id);
    if (idx >= 0) remaining.splice(idx, 1);
    progress = true;
  }
}

for (const state of droneStates) {
  if (state.path.length) {
    flightManifest.push({ drone_id: state.drone.id, path: state.path });
  }
}

console.log(JSON.stringify({ flight_manifest: flightManifest }));