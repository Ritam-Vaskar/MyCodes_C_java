# Drone Fleet Routing with Dynamic No-Fly Zones

## Background
In 2026, cities enforce dynamic no-fly zones for autonomous delivery drones. These zones activate and deactivate over time, requiring careful planning to avoid violations while meeting delivery deadlines and battery constraints.

## Problem Statement
Build a routing engine that assigns and routes a fleet of drones from a central warehouse to complete deliveries on a 2D grid. Drones must avoid active no-fly zones, respect battery limits, and satisfy delivery deadlines. Each drone starts at the warehouse (map center) and can carry multiple packages if the total weight is within its payload limit.

## Input Format
A JSON file with this structure:

{
  "map_size": [Width, Height],
  "drones": [
    {"id": "drone_1", "max_payload": 1.0}
  ],
  "deliveries": [
    {"id": "d1", "x": 20, "y": 30, "weight": 0.3, "deadline": 200}
  ],
  "charging_stations": [
    {"x": 50, "y": 50, "slots": 2}
  ],
  "no_fly_zones": [
    {
      "shape": "circle",
      "center": [80, 80],
      "radius": 15,
      "T_start": 0,
      "T_end": 150
    },
    {
      "shape": "rectangle",
      "corners": [[120, 120], [140, 160]],
      "T_start": 50,
      "T_end": 300
    }
  ]
}

### Field Definitions
- map_size: [Width, Height] of the grid. Warehouse is at (Width/2, Height/2).
- drones: list of drones with id and max_payload.
- deliveries: list of delivery requests with location, weight, and deadline.
- charging_stations: list of station locations and slot limits.
- no_fly_zones: list of time-windowed circular or rectangular zones.

## Output Format
A JSON flight manifest:

{
  "flight_manifest": [
    {
      "drone_id": "drone_1",
      "path": [
        {"x": 50, "y": 50, "t": 0.0, "action": "PICKUP", "delivery_ids": ["d1"]},
        {"x": 20, "y": 30, "t": 42.4, "action": "DELIVER", "delivery_id": "d1"},
        {"x": 50, "y": 50, "t": 92.0, "action": "RETURN"}
      ]
    }
  ]
}

### Action Types
- PICKUP: pick up packages at the warehouse (includes delivery_ids).
- DELIVER: deliver a single package (includes delivery_id).
- CHARGE: arrive at a charging station.
- CHARGE_COMPLETE: finish charging and depart.
- WAIT: wait at the current position until an NFZ expires.
- WAYPOINT: intermediate navigation point (optional).
- RETURN: end of trip at warehouse or charging station.

## Constraints
- Speed: 1 distance unit per timestep.
- Battery: 500 energy units, full at start and on warehouse return.
- Charge rate: 2 energy units per timestep.
- Energy per leg: distance * (1 + current_payload_weight).
- No-fly zones are active only in [T_start, T_end].
- Drones cannot enter active zones; they may wait to resume.
- Deadlines are strict.

## Implementation Notes
- Greedy assignment by earliest deadline to capable drones.
- One delivery per trip for safety and deadline compliance.
- Straight-line travel with NFZ-aware waiting (no detours).
- Optional charging at the nearest station if return energy is insufficient.

## Build and Run (Example)
- Compile: g++ -std=c++17 main.cpp -ljsoncpp
- Run: cat input.json | ./a.exe
