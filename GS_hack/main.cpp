// Start of HEAD
#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <sstream>
#include <algorithm>
#include <json/json.h>

using namespace std;

struct Delivery {
    string id;
    double x;
    double y;
    double weight;
    double deadline;
    int assigned_drone;
};

struct Drone {
    string id;
    double max_payload;
};

struct NFZ {
    string shape;
    double cx, cy, radius;
    double x1, y1, x2, y2;
    double t_start, t_end;
};

struct Point {
    double x;
    double y;
};

static const double BATTERY_CAPACITY = 500.0;
static const double CHARGE_RATE = 2.0;
static const double SPEED = 1.0;
static const double EPS = 1e-9;

// End of HEAD

// Start of BODY

static double dist_pt(const Point &a, const Point &b) {
    double dx = a.x - b.x;
    double dy = a.y - b.y;
    return sqrt(dx * dx + dy * dy);
}

static bool segment_circle_interval(const Point &a, const Point &b, double cx, double cy, double r, double &s_enter, double &s_exit) {
    double dx = b.x - a.x;
    double dy = b.y - a.y;
    double fx = a.x - cx;
    double fy = a.y - cy;

    double A = dx * dx + dy * dy;
    if (A < EPS) {
        double dist2 = fx * fx + fy * fy;
        if (dist2 <= r * r) {
            s_enter = 0.0;
            s_exit = 0.0;
            return true;
        }
        return false;
    }

    double B = 2.0 * (fx * dx + fy * dy);
    double C = fx * fx + fy * fy - r * r;
    double disc = B * B - 4.0 * A * C;
    if (disc < 0.0) {
        return false;
    }

    double sqrt_disc = sqrt(max(0.0, disc));
    double t1 = (-B - sqrt_disc) / (2.0 * A);
    double t2 = (-B + sqrt_disc) / (2.0 * A);
    double t_enter = min(t1, t2);
    double t_exit = max(t1, t2);

    double t0 = max(0.0, t_enter);
    double t1c = min(1.0, t_exit);
    if (t0 > t1c) {
        return false;
    }

    double len = sqrt(A);
    s_enter = t0 * len;
    s_exit = t1c * len;
    return true;
}

static bool segment_rect_interval(const Point &a, const Point &b, double x_min, double y_min, double x_max, double y_max, double &s_enter, double &s_exit) {
    double dx = b.x - a.x;
    double dy = b.y - a.y;
    double t0 = 0.0;
    double t1 = 1.0;

    auto clip = [&](double p, double q, double &t0_ref, double &t1_ref) -> bool {
        if (fabs(p) < EPS) {
            return q >= 0.0;
        }
        double r = q / p;
        if (p < 0.0) {
            if (r > t1_ref) return false;
            if (r > t0_ref) t0_ref = r;
        } else {
            if (r < t0_ref) return false;
            if (r < t1_ref) t1_ref = r;
        }
        return true;
    };

    if (!clip(-dx, a.x - x_min, t0, t1)) return false;
    if (!clip(dx, x_max - a.x, t0, t1)) return false;
    if (!clip(-dy, a.y - y_min, t0, t1)) return false;
    if (!clip(dy, y_max - a.y, t0, t1)) return false;

    if (t0 > t1) return false;

    double len = dist_pt(a, b);
    s_enter = t0 * len;
    s_exit = t1 * len;
    return true;
}

static bool nfz_segment_interval(const NFZ &nfz, const Point &a, const Point &b, double &s_enter, double &s_exit) {
    if (nfz.shape == "circle") {
        return segment_circle_interval(a, b, nfz.cx, nfz.cy, nfz.radius, s_enter, s_exit);
    }
    return segment_rect_interval(a, b, nfz.x1, nfz.y1, nfz.x2, nfz.y2, s_enter, s_exit);
}

static double earliest_safe_start(const Point &a, const Point &b, double t0, const vector<NFZ> &nfzs) {
    double start = t0;
    bool changed = true;
    int guard = 0;
    while (changed && guard < 1000) {
        changed = false;
        guard++;
        for (const auto &nfz : nfzs) {
            double s_enter = 0.0, s_exit = 0.0;
            if (!nfz_segment_interval(nfz, a, b, s_enter, s_exit)) {
                continue;
            }
            double enter_time = start + s_enter / SPEED;
            double exit_time = start + s_exit / SPEED;
            bool overlap = (enter_time <= nfz.t_end + EPS) && (exit_time >= nfz.t_start - EPS);
            if (overlap) {
                double new_start = nfz.t_end - s_enter / SPEED + 1e-6;
                if (new_start > start + EPS) {
                    start = new_start;
                    changed = true;
                }
            }
        }
    }
    return start;
}

static bool add_leg(Json::Value &path, const Point &from, const Point &to, double payload, double &time, double &battery, const vector<NFZ> &nfzs) {
    double start = earliest_safe_start(from, to, time, nfzs);
    if (start > time + EPS) {
        Json::Value wait_step;
        wait_step["x"] = from.x;
        wait_step["y"] = from.y;
        wait_step["t"] = start;
        wait_step["action"] = "WAIT";
        path.append(wait_step);
        time = start;
    }

    double d = dist_pt(from, to);
    double energy = d * (1.0 + payload);
    if (battery + EPS < energy) {
        return false;
    }

    battery -= energy;
    time += d / SPEED;
    return true;
}

struct TripResult {
    bool success;
    bool infeasible;
    Json::Value path;
    double end_time;
    vector<int> delivered;
    vector<int> missed;
};

static void order_trip(vector<int> &trip, const vector<Delivery> &deliveries, const Point &warehouse);
static TripResult simulate_trip(const vector<int> &trip,
                                const vector<Delivery> &deliveries,
                                const Point &warehouse,
                                const vector<Point> &charging_stations,
                                const vector<NFZ> &nfzs,
                                double start_time);

static vector<int> build_trip(const vector<int> &remaining,
                              const vector<Delivery> &deliveries,
                              const Drone &drone,
                              const Point &warehouse,
                              const vector<Point> &charging_stations,
                              const vector<NFZ> &nfzs,
                              double start_time) {
    vector<int> candidates = remaining;
    sort(candidates.begin(), candidates.end(), [&](int a, int b) {
        return deliveries[a].deadline < deliveries[b].deadline;
    });

    vector<int> trip;
    double payload = 0.0;
    for (int idx : candidates) {
        const Delivery &del = deliveries[idx];
        if (payload + del.weight > drone.max_payload + EPS) {
            continue;
        }
        double dist_to_del = dist_pt(warehouse, Point{del.x, del.y});
        double energy_to_del = dist_to_del * (1.0 + payload + del.weight);
        double energy_to_wh = dist_to_del;
        if (energy_to_del + energy_to_wh > BATTERY_CAPACITY + EPS) {
            continue;
        }
        vector<int> trial = trip;
        trial.push_back(idx);
        order_trip(trial, deliveries, warehouse);
        TripResult sim = simulate_trip(trial, deliveries, warehouse, charging_stations, nfzs, start_time);
        if (sim.infeasible) {
            continue;
        }
        trip.swap(trial);
        payload += del.weight;
    }
    return trip;
}

static void order_trip(vector<int> &trip, const vector<Delivery> &deliveries, const Point &warehouse) {
    sort(trip.begin(), trip.end(), [&](int a, int b) {
        if (fabs(deliveries[a].weight - deliveries[b].weight) > EPS) {
            return deliveries[a].weight > deliveries[b].weight;
        }
        double da = dist_pt(warehouse, Point{deliveries[a].x, deliveries[a].y});
        double db = dist_pt(warehouse, Point{deliveries[b].x, deliveries[b].y});
        return da < db;
    });
}

static TripResult simulate_trip(const vector<int> &trip,
                                const vector<Delivery> &deliveries,
                                const Point &warehouse,
                                const vector<Point> &charging_stations,
                                const vector<NFZ> &nfzs,
                                double start_time) {
    TripResult res;
    res.success = false;
    res.infeasible = false;
    res.end_time = start_time;
    res.path = Json::Value(Json::arrayValue);

    if (trip.empty()) {
        res.infeasible = true;
        return res;
    }

    double payload = 0.0;
    Json::Value ids(Json::arrayValue);
    for (int idx : trip) {
        payload += deliveries[idx].weight;
        ids.append(deliveries[idx].id);
    }

    Json::Value pickup_step;
    pickup_step["x"] = warehouse.x;
    pickup_step["y"] = warehouse.y;
    pickup_step["t"] = start_time;
    pickup_step["action"] = "PICKUP";
    pickup_step["delivery_ids"] = ids;
    res.path.append(pickup_step);

    double time = start_time;
    double battery = BATTERY_CAPACITY;
    Point pos = warehouse;

    for (int idx : trip) {
        const Delivery &del = deliveries[idx];
        Point target{del.x, del.y};
        if (!add_leg(res.path, pos, target, payload, time, battery, nfzs)) {
            res.infeasible = true;
            return res;
        }

        Json::Value deliver_step;
        deliver_step["x"] = target.x;
        deliver_step["y"] = target.y;
        deliver_step["t"] = time;
        deliver_step["action"] = "DELIVER";
        deliver_step["delivery_id"] = del.id;
        res.path.append(deliver_step);

        if (time > del.deadline + EPS) {
            res.missed.push_back(idx);
        } else {
            res.delivered.push_back(idx);
        }

        payload -= del.weight;
        pos = target;
    }

    if (!res.missed.empty()) {
        res.infeasible = true;
        return res;
    }

    double need_return = dist_pt(pos, warehouse) * (1.0 + payload);
    if (battery + EPS < need_return) {
        if (charging_stations.empty()) {
            res.infeasible = true;
            return res;
        }
        double best_d = 1e18;
        int best_idx = -1;
        for (int i = 0; i < (int)charging_stations.size(); ++i) {
            double d = dist_pt(pos, charging_stations[i]);
            if (d < best_d) {
                best_d = d;
                best_idx = i;
            }
        }
        Point station = charging_stations[best_idx];
        if (!add_leg(res.path, pos, station, payload, time, battery, nfzs)) {
            res.infeasible = true;
            return res;
        }

        Json::Value charge_step;
        charge_step["x"] = station.x;
        charge_step["y"] = station.y;
        charge_step["t"] = time;
        charge_step["action"] = "CHARGE";
        res.path.append(charge_step);

        double need = dist_pt(station, warehouse);
        if (battery + EPS < need) {
            double deficit = need - battery;
            double charge_time = ceil(deficit / CHARGE_RATE);
            time += charge_time;
            battery += charge_time * CHARGE_RATE;

            Json::Value charge_done;
            charge_done["x"] = station.x;
            charge_done["y"] = station.y;
            charge_done["t"] = time;
            charge_done["action"] = "CHARGE_COMPLETE";
            res.path.append(charge_done);
        }

        pos = station;
    }

    if (!add_leg(res.path, pos, warehouse, payload, time, battery, nfzs)) {
        res.infeasible = true;
        return res;
    }

    Json::Value return_step;
    return_step["x"] = warehouse.x;
    return_step["y"] = warehouse.y;
    return_step["t"] = time;
    return_step["action"] = "RETURN";
    res.path.append(return_step);

    res.success = true;
    res.end_time = time;
    return res;
}

int main() {
    string input_str((istreambuf_iterator<char>(cin)), istreambuf_iterator<char>());
    Json::Value input_data;
    Json::CharReaderBuilder rb;
    string errs;
    istringstream ss(input_str);
    Json::parseFromStream(rb, ss, &input_data, &errs);

    double mapW = input_data["map_size"][0].asDouble();
    double mapH = input_data["map_size"][1].asDouble();
    Point warehouse{mapW / 2.0, mapH / 2.0};

    vector<Drone> drones;
    for (const auto &d : input_data["drones"]) {
        Drone dr;
        dr.id = d["id"].asString();
        dr.max_payload = d["max_payload"].asDouble();
        drones.push_back(dr);
    }

    vector<Delivery> deliveries;
    for (const auto &d : input_data["deliveries"]) {
        Delivery del;
        del.id = d["id"].asString();
        del.x = d["x"].asDouble();
        del.y = d["y"].asDouble();
        del.weight = d["weight"].asDouble();
        del.deadline = d["deadline"].asDouble();
        del.assigned_drone = -1;
        deliveries.push_back(del);
    }

    vector<NFZ> nfzs;
    Json::Value nfz_list = input_data.get("no_fly_zones", Json::Value(Json::arrayValue));
    for (const auto &z : nfz_list) {
        NFZ nfz;
        nfz.shape = z["shape"].asString();
        nfz.t_start = z["T_start"].asDouble();
        nfz.t_end = z["T_end"].asDouble();
        if (nfz.shape == "circle") {
            nfz.cx = z["center"][0].asDouble();
            nfz.cy = z["center"][1].asDouble();
            nfz.radius = z["radius"].asDouble();
        } else {
            nfz.x1 = min(z["corners"][0][0].asDouble(), z["corners"][1][0].asDouble());
            nfz.y1 = min(z["corners"][0][1].asDouble(), z["corners"][1][1].asDouble());
            nfz.x2 = max(z["corners"][0][0].asDouble(), z["corners"][1][0].asDouble());
            nfz.y2 = max(z["corners"][0][1].asDouble(), z["corners"][1][1].asDouble());
        }
        nfzs.push_back(nfz);
    }

    vector<Point> charging_stations;
    Json::Value cs_list = input_data.get("charging_stations", Json::Value(Json::arrayValue));
    for (const auto &cs : cs_list) {
        charging_stations.push_back(Point{cs["x"].asDouble(), cs["y"].asDouble()});
    }

    Json::Value flight_manifest(Json::arrayValue);
    vector<Json::Value> drone_paths(drones.size(), Json::Value(Json::arrayValue));
    vector<double> drone_times(drones.size(), 0.0);
    vector<int> remaining(deliveries.size());
    for (int i = 0; i < (int)deliveries.size(); ++i) remaining[i] = i;

    bool progress = true;
    while (progress && !remaining.empty()) {
        progress = false;
        for (int di = 0; di < (int)drones.size(); ++di) {
            vector<int> trip = build_trip(remaining, deliveries, drones[di], warehouse, charging_stations, nfzs, drone_times[di]);
            if (trip.empty()) continue;

            TripResult res = simulate_trip(trip, deliveries, warehouse, charging_stations, nfzs, drone_times[di]);
            if (res.infeasible) {
                vector<int> filtered;
                for (int idx : remaining) {
                    if (find(res.missed.begin(), res.missed.end(), idx) == res.missed.end()) {
                        filtered.push_back(idx);
                    }
                }
                remaining.swap(filtered);
                continue;
            }

            if (res.success) {
                for (const auto &step : res.path) {
                    drone_paths[di].append(step);
                }
                drone_times[di] = res.end_time;
                vector<int> filtered;
                for (int idx : remaining) {
                    if (find(res.delivered.begin(), res.delivered.end(), idx) == res.delivered.end()) {
                        filtered.push_back(idx);
                    }
                }
                remaining.swap(filtered);
                progress = true;
            }
        }
    }

    for (int di = 0; di < (int)drones.size(); ++di) {
        if (drone_paths[di].empty()) continue;
        Json::Value drone_entry;
        drone_entry["drone_id"] = drones[di].id;
        drone_entry["path"] = drone_paths[di];
        flight_manifest.append(drone_entry);
    }

    Json::Value output;
    output["flight_manifest"] = flight_manifest;
    Json::StreamWriterBuilder wb;
    wb["indentation"] = "";
    cout << Json::writeString(wb, output) << endl;
    return 0;
}

// End of BODY

// Start of TAIL
// End of TAIL
