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

// --- NFZ geometric intersection ---
// Returns parametric s_enter/s_exit in distance units along segment A->B
// where the segment intersects the NFZ shape.

static bool segment_circle_interval(const Point &a, const Point &b,
    double cx, double cy, double r, double &s_enter, double &s_exit)
{
    double dx = b.x - a.x;
    double dy = b.y - a.y;
    double fx = a.x - cx;
    double fy = a.y - cy;
    double A = dx * dx + dy * dy;
    if (A < EPS) {
        double dist2 = fx * fx + fy * fy;
        if (dist2 <= r * r + EPS) {
            s_enter = 0.0;
            s_exit = 0.0;
            return true;
        }
        return false;
    }
    double B = 2.0 * (fx * dx + fy * dy);
    double C = fx * fx + fy * fy - r * r;
    double disc = B * B - 4.0 * A * C;
    if (disc < 0.0) return false;

    double sqrt_disc = sqrt(max(0.0, disc));
    double t1 = (-B - sqrt_disc) / (2.0 * A);
    double t2 = (-B + sqrt_disc) / (2.0 * A);
    double t_lo = min(t1, t2);
    double t_hi = max(t1, t2);
    double s0 = max(0.0, t_lo);
    double s1 = min(1.0, t_hi);
    if (s0 > s1 + EPS) return false;

    double len = sqrt(A);
    s_enter = s0 * len;
    s_exit = s1 * len;
    return true;
}

static bool segment_rect_interval(const Point &a, const Point &b,
    double x_min, double y_min, double x_max, double y_max,
    double &s_enter, double &s_exit)
{
    double dx = b.x - a.x;
    double dy = b.y - a.y;
    double t0 = 0.0;
    double t1 = 1.0;

    auto clip = [&](double p, double q, double &t0_ref, double &t1_ref) -> bool {
        if (fabs(p) < EPS) {
            return q >= -EPS;
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
    if (t0 > t1 + EPS) return false;

    double len = dist_pt(a, b);
    s_enter = t0 * len;
    s_exit = t1 * len;
    return true;
}

static bool nfz_segment_interval(const NFZ &nfz, const Point &a, const Point &b,
    double &s_enter, double &s_exit)
{
    if (nfz.shape == "circle") {
        return segment_circle_interval(a, b, nfz.cx, nfz.cy, nfz.radius, s_enter, s_exit);
    }
    return segment_rect_interval(a, b, nfz.x1, nfz.y1, nfz.x2, nfz.y2, s_enter, s_exit);
}

// The old earliest_safe_start function was replaced by earliest_safe_start_fast and is no longer needed.

// --- Path segment: generates waypoints for a leg, handling NFZ avoidance ---

struct WayPoint {
    double x, y, t;
    bool is_wait;     // true = WAIT at same position
    bool is_waypoint; // true = WAYPOINT (intermediate navigation)
};

vector<Point> global_wps;

struct EdgeNFZ {
    int nfz_idx;
    double s_enter;
    double s_exit;
};

static vector<EdgeNFZ> static_edge_nfzs[1000][1000];
static double static_dist[1000][1000];

static void precompute_static_edges(const vector<NFZ> &nfzs) {
    int W = global_wps.size();
    if (W > 1000) W = 1000; // safety bound
    for (int i = 0; i < W; ++i) {
        for (int j = 0; j < W; ++j) {
            static_dist[i][j] = dist_pt(global_wps[i], global_wps[j]);
            if (i == j) continue;
            for (int k = 0; k < (int)nfzs.size(); ++k) {
                double s_en, s_ex;
                if (nfz_segment_interval(nfzs[k], global_wps[i], global_wps[j], s_en, s_ex)) {
                    static_edge_nfzs[i][j].push_back({k, s_en, s_ex});
                }
            }
        }
    }
}

static double earliest_safe_start_fast(double t0, const vector<NFZ> &nfzs, const vector<EdgeNFZ> &intersecting)
{
    double start = t0;
    bool changed = true;
    int guard = 0;
    while (changed && guard < 500) {
        changed = false;
        guard++;
        for (const auto &en : intersecting) {
            const auto &nfz = nfzs[en.nfz_idx];
            double enter_time = start + en.s_enter / SPEED;
            double exit_time = start + en.s_exit / SPEED;
            if (enter_time <= nfz.t_end + EPS && exit_time >= nfz.t_start - EPS) {
                double new_start = nfz.t_end - en.s_enter / SPEED + 1e-6;
                if (new_start > start + EPS) {
                    start = new_start;
                    changed = true;
                }
            }
        }
    }
    return start;
}

static vector<EdgeNFZ> get_dynamic_edge_nfzs(const Point &a, const Point &b, const vector<NFZ> &nfzs) {
    vector<EdgeNFZ> res;
    for(int k = 0; k < (int)nfzs.size(); ++k) {
        double s_en, s_ex;
        if(nfz_segment_interval(nfzs[k], a, b, s_en, s_ex)) {
            res.push_back({k, s_en, s_ex});
        }
    }
    return res;
}

// Find path from A to B starting at time t0, with NFZ avoidance using Dijkstra.
static vector<WayPoint> find_safe_path(const Point &a, const Point &b, double t0,
    const vector<NFZ> &nfzs)
{
    int N = 2 + global_wps.size();
    
    struct PathNode {
        double t_arrive;
        double t_depart;
        int parent;
    };
    vector<PathNode> nodes(N, {1e18, 1e18, -1});
    nodes[0].t_arrive = t0;

    vector<bool> vis(N, false);
    for (int step = 0; step < N; step++) {
        int u = -1;
        double best_t = 1e18;
        for (int i = 0; i < N; i++) {
            if (!vis[i] && nodes[i].t_arrive < best_t) {
                best_t = nodes[i].t_arrive;
                u = i;
            }
        }
        if (u == -1 || u == 1) break; 
        vis[u] = true;

        Point pu = (u == 0) ? a : ((u == 1) ? b : global_wps[u - 2]);

        for (int v = 0; v < N; v++) {
            if (vis[v]) continue;
            Point pv = (v == 0) ? a : ((v == 1) ? b : global_wps[v - 2]);
            
            double dist;
            vector<EdgeNFZ> edge_nfzs;
            if (u >= 2 && v >= 2 && u - 2 < 1000 && v - 2 < 1000) {
                dist = static_dist[u - 2][v - 2];
                edge_nfzs = static_edge_nfzs[u - 2][v - 2];
            } else {
                dist = dist_pt(pu, pv);
                edge_nfzs = get_dynamic_edge_nfzs(pu, pv, nfzs);
            }
            
            double t_dep = earliest_safe_start_fast(nodes[u].t_arrive, nfzs, edge_nfzs);
            double t_arr = t_dep + dist / SPEED;
            
            if (t_arr < nodes[v].t_arrive) {
                nodes[v].t_arrive = t_arr;
                nodes[v].t_depart = t_dep;
                nodes[v].parent = u;
            }
        }
    }

    if (nodes[1].parent == -1) return {};

    vector<int> path_idx;
    int curr = 1;
    while (curr != -1) {
        path_idx.push_back(curr);
        curr = nodes[curr].parent;
    }
    reverse(path_idx.begin(), path_idx.end());

    vector<WayPoint> result;
    for (int i = 0; i < (int)path_idx.size(); i++) {
        int u = path_idx[i];
        Point pu = (u == 0) ? a : ((u == 1) ? b : global_wps[u - 2]);
        if (i == 0) {
            result.push_back({pu.x, pu.y, t0, false, false});
        } else {
            int p = path_idx[i-1];
            double t_dep = nodes[u].t_depart;
            double t_arr = nodes[u].t_arrive;
            
            if (t_dep > nodes[p].t_arrive + EPS) {
                Point pp = (p == 0) ? a : ((p == 1) ? b : global_wps[p - 2]);
                result.push_back({pp.x, pp.y, t_dep, true, false});
            }
            bool is_wp = (u != 1);
            result.push_back({pu.x, pu.y, t_arr, false, is_wp});
        }
    }
    return result;
}

static double get_path_dist(const vector<WayPoint> &wps) {
    if (wps.empty()) return 1e18;
    double d = 0;
    for (int i = 1; i < (int)wps.size(); i++) {
        if (!wps[i].is_wait) {
            d += dist_pt({wps[i-1].x, wps[i-1].y}, {wps[i].x, wps[i].y});
        }
    }
    return d;
}

static bool add_leg_wps(Json::Value &path, const vector<WayPoint> &wps,
    double payload, double &time, double &battery)
{
    if (wps.empty()) return false;
    double total_dist = get_path_dist(wps);
    double energy = total_dist * (1.0 + payload);
    if (battery + EPS < energy) return false;

    for (int i = 1; i < (int)wps.size() - 1; i++) {
        Json::Value step;
        step["x"] = wps[i].x;
        step["y"] = wps[i].y;
        step["t"] = wps[i].t;
        step["action"] = wps[i].is_wait ? "WAIT" : "WAYPOINT";
        path.append(step);
    }

    battery -= energy;
    time = wps.back().t;
    return true;
}

// --- Trip simulation ---

struct TripResult {
    bool success;
    bool infeasible;
    Json::Value path;
    double end_time;
    double total_energy;
    vector<int> delivered;
};

static TripResult simulate_trip(const vector<int> &trip,
    const vector<Delivery> &deliveries,
    const Point &warehouse,
    const vector<Point> &charging_stations,
    const vector<NFZ> &nfzs,
    double start_time)
{
    TripResult res;
    res.success = false;
    res.infeasible = false;
    res.end_time = start_time;
    res.total_energy = 0;
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
    double energy_used = 0;
    Point pos = warehouse;

    for (int idx : trip) {
        const Delivery &del = deliveries[idx];
        Point target{del.x, del.y};
        
        auto wps = find_safe_path(pos, target, time, nfzs);
        double bat_before = battery;
        if (!add_leg_wps(res.path, wps, payload, time, battery)) {
            res.infeasible = true; return res;
        }
        energy_used += (bat_before - battery);

        if (time > del.deadline + EPS) {
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

        res.delivered.push_back(idx);
        payload -= del.weight;
        pos = target;
    }

    // Return logic with accurate energy
    auto wps_ret = find_safe_path(pos, warehouse, time, nfzs);
    double need_return = get_path_dist(wps_ret) * (1.0 + payload); // payload is 0
    
    if (battery + EPS < need_return) {
        // Need to charge
        int best_sta = -1;
        double best_total = 1e18;
        vector<WayPoint> best_sta_wps;
        vector<WayPoint> best_wh_wps;

        for (int i = 0; i < (int)charging_stations.size(); ++i) {
            auto wps_to_sta = find_safe_path(pos, charging_stations[i], time, nfzs);
            if (wps_to_sta.empty()) continue;
            double d_to_sta = get_path_dist(wps_to_sta);
            double e_to_sta = d_to_sta * (1.0 + payload);
            if (battery + EPS < e_to_sta) continue;

            double arr_sta = time + d_to_sta; 
            double d_sta_wh_est = dist_pt(charging_stations[i], warehouse);
            double e_sta_wh_est = d_sta_wh_est * 1.0; 
            double deficit = e_sta_wh_est - (battery - e_to_sta);
            double charge_time = deficit > 0 ? ceil(deficit / CHARGE_RATE) : 0;
            double dep_sta = arr_sta + charge_time;

            auto wps_sta_wh = find_safe_path(charging_stations[i], warehouse, dep_sta, nfzs);
            if (wps_sta_wh.empty()) continue;
            double d_sta_wh = get_path_dist(wps_sta_wh);
            
            double total_dist = d_to_sta + d_sta_wh;
            if (total_dist < best_total) {
                best_total = total_dist;
                best_sta = i;
                best_sta_wps = wps_to_sta;
                best_wh_wps = wps_sta_wh;
            }
        }

        if (best_sta < 0) {
            res.infeasible = true;
            return res;
        }

        Point station = charging_stations[best_sta];
        double bat_before = battery;
        if (!add_leg_wps(res.path, best_sta_wps, payload, time, battery)) {
            res.infeasible = true; return res;
        }
        energy_used += (bat_before - battery);

        Json::Value charge_step;
        charge_step["x"] = station.x;
        charge_step["y"] = station.y;
        charge_step["t"] = time;
        charge_step["action"] = "CHARGE";
        res.path.append(charge_step);

        double deficit = get_path_dist(best_wh_wps) * 1.0 - battery;
        if (deficit > 0) {
            double charge_time = ceil(deficit / CHARGE_RATE);
            time += charge_time;
            battery += charge_time * CHARGE_RATE;
        }

        Json::Value charge_done;
        charge_done["x"] = station.x;
        charge_done["y"] = station.y;
        charge_done["t"] = time;
        charge_done["action"] = "CHARGE_COMPLETE";
        res.path.append(charge_done);

        pos = station;
        wps_ret = find_safe_path(pos, warehouse, time, nfzs);
    }

    double bat_before = battery;
    if (!add_leg_wps(res.path, wps_ret, payload, time, battery)) {
        res.infeasible = true;
        return res;
    }
    energy_used += (bat_before - battery);

    Json::Value return_step;
    return_step["x"] = warehouse.x;
    return_step["y"] = warehouse.y;
    return_step["t"] = time;
    return_step["action"] = "RETURN";
    res.path.append(return_step);

    res.success = true;
    res.end_time = time;
    res.total_energy = energy_used;
    return res;
}

// --- Trip ordering: try permutations for small sets, nearest-neighbor for larger ---

struct OrderEval {
    int on_time;
    double energy;
    double makespan;
    bool feasible;
};

static OrderEval eval_order(const vector<int> &order,
    const vector<Delivery> &deliveries,
    const Point &warehouse,
    const vector<Point> &charging_stations,
    double start_time)
{
    OrderEval ev;
    ev.on_time = 0;
    ev.energy = 0;
    ev.makespan = 0;
    ev.feasible = true;

    double payload = 0;
    for (int idx : order) payload += deliveries[idx].weight;

    double t = start_time;
    double battery = BATTERY_CAPACITY;
    Point pos = warehouse;

    for (int idx : order) {
        const Delivery &del = deliveries[idx];
        Point target{del.x, del.y};
        double d = dist_pt(pos, target);
        double e = d * (1.0 + payload);
        battery -= e;
        ev.energy += e;
        t += d;

        if (battery < -EPS) { ev.feasible = false; break; }
        if (t <= del.deadline + EPS) ev.on_time++;
        else { ev.feasible = false; break; }

        payload -= del.weight;
        pos = target;
    }

    if (ev.feasible) {
        double d_ret = dist_pt(pos, warehouse);
        double e_ret = d_ret * (1.0 + payload);
        if (battery + EPS < e_ret) {
            bool can_charge = false;
            for (const auto &st : charging_stations) {
                double d_st = dist_pt(pos, st);
                double e_st = d_st * (1.0 + payload);
                if (battery + EPS >= e_st) {
                    can_charge = true;
                    double d_st_wh = dist_pt(st, warehouse);
                    ev.energy += e_st + d_st_wh * (1.0 + payload);
                    t += d_st + d_st_wh;
                    break;
                }
            }
            if (!can_charge) ev.feasible = false;
        } else {
            ev.energy += e_ret;
            t += d_ret;
        }
    }

    ev.makespan = t - start_time;
    return ev;
}

static vector<int> best_ordering(const vector<int> &candidates,
    const vector<Delivery> &deliveries,
    const Point &warehouse,
    const vector<Point> &charging_stations,
    double start_time)
{
    int n = (int)candidates.size();
    if (n == 0) return {};
    if (n == 1) return candidates;

    if (n <= 8) {
        vector<int> perm(n);
        for (int i = 0; i < n; i++) perm[i] = i;

        vector<int> best_order;
        int best_on_time = -1;
        double best_score = -1e18;

        do {
            vector<int> order(n);
            for (int i = 0; i < n; i++) order[i] = candidates[perm[i]];

            OrderEval ev = eval_order(order, deliveries, warehouse, charging_stations, start_time);
            if (!ev.feasible) continue;

            double score = ev.on_time * 1000.0 - ev.energy * 0.1 - ev.makespan * 0.05;
            if (ev.on_time > best_on_time || (ev.on_time == best_on_time && score > best_score)) {
                best_on_time = ev.on_time;
                best_score = score;
                best_order = order;
            }
        } while (next_permutation(perm.begin(), perm.end()));

        if (!best_order.empty()) return best_order;
    }

    vector<bool> used(n, false);
    vector<int> result;
    Point pos = warehouse;

    for (int step = 0; step < n; step++) {
        int best_i = -1;
        double best_val = 1e18;
        for (int i = 0; i < n; i++) {
            if (used[i]) continue;
            double d = dist_pt(pos, {deliveries[candidates[i]].x, deliveries[candidates[i]].y});
            double t = start_time + d; // Rough estimate of arrival time
            double slack = deliveries[candidates[i]].deadline - t;
            
            double val;
            if (slack < -EPS) val = 1e9 + d;
            else val = d + 0.1 * deliveries[candidates[i]].deadline;
            
            if (val < best_val) {
                best_val = val;
                best_i = i;
            }
        }
        if (best_i < 0) break;
        used[best_i] = true;
        result.push_back(candidates[best_i]);
        pos = {deliveries[candidates[best_i]].x, deliveries[candidates[best_i]].y};
    }

    return result;
}

// --- Build a trip for a drone ---

static vector<int> build_trip(const vector<int> &remaining,
    const vector<Delivery> &deliveries,
    const Drone &drone,
    const Point &warehouse,
    const vector<Point> &charging_stations,
    const vector<NFZ> &nfzs,
    double start_time)
{
    vector<int> candidates = remaining;
    sort(candidates.begin(), candidates.end(), [&](int a, int b) {
        return deliveries[a].deadline < deliveries[b].deadline;
    });

    vector<int> best_trip;
    double best_trip_score = -1e18;
    int tested_anchors = 0;

    for (int anchor : candidates) {
        if (tested_anchors >= 20) break;
        if (deliveries[anchor].weight > drone.max_payload + EPS) continue;
        double d = dist_pt(warehouse, {deliveries[anchor].x, deliveries[anchor].y});
        if (start_time + d > deliveries[anchor].deadline + EPS) continue;

        vector<int> trip_cands;
        trip_cands.push_back(anchor);
        double trip_weight = deliveries[anchor].weight;

        Point anchor_pt{deliveries[anchor].x, deliveries[anchor].y};
        vector<pair<double, int>> nearby;
        for (int idx : candidates) {
            if (idx == anchor) continue;
            if (trip_weight + deliveries[idx].weight > drone.max_payload + EPS) continue;
            double dist_to_anchor = dist_pt(anchor_pt, {deliveries[idx].x, deliveries[idx].y});
            nearby.push_back({dist_to_anchor, idx});
        }
        sort(nearby.begin(), nearby.end());

        const int MAX_TRIP = 8;
        for (const auto &p : nearby) {
            if ((int)trip_cands.size() >= MAX_TRIP) break;
            int idx = p.second;
            if (trip_weight + deliveries[idx].weight > drone.max_payload + EPS) continue;

            vector<int> test_trip = trip_cands;
            test_trip.push_back(idx);

            vector<int> test_order = best_ordering(test_trip, deliveries, warehouse,
                charging_stations, start_time);

            if (!test_order.empty()) {
                OrderEval ev = eval_order(test_order, deliveries, warehouse,
                    charging_stations, start_time);
                if (ev.feasible && ev.on_time == (int)test_trip.size()) {
                    trip_cands.push_back(idx);
                    trip_weight += deliveries[idx].weight;
                }
            }
        }

        vector<int> ordered = best_ordering(trip_cands, deliveries, warehouse,
            charging_stations, start_time);

        if (ordered.empty()) ordered = {anchor};

        TripResult sim = simulate_trip(ordered, deliveries, warehouse, charging_stations,
            nfzs, start_time);

        vector<int> valid_trip;
        if (sim.success) {
            valid_trip = ordered;
        } else {
            while (ordered.size() > 1) {
                ordered.pop_back();
                sim = simulate_trip(ordered, deliveries, warehouse, charging_stations,
                    nfzs, start_time);
                if (sim.success) {
                    valid_trip = ordered;
                    break;
                }
            }
            if (valid_trip.empty()) {
                sim = simulate_trip({anchor}, deliveries, warehouse, charging_stations,
                    nfzs, start_time);
                if (sim.success) valid_trip = {anchor};
            }
        }

        if (!valid_trip.empty()) {
            double score = valid_trip.size() * 1000.0 - sim.end_time * 0.01;
            if (score > best_trip_score) {
                best_trip_score = score;
                best_trip = valid_trip;
            }
        }
        tested_anchors++;
    }

    return best_trip;
}

// --- Main ---

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
        nfz.cx = nfz.cy = nfz.radius = 0;
        nfz.x1 = nfz.y1 = nfz.x2 = nfz.y2 = 0;
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

    global_wps.clear();
    for (const auto &nfz : nfzs) {
        double margin = 1e-3;
        if (nfz.shape == "circle") {
            double R = nfz.radius + margin;
            for (int d = 0; d < 8; d++) {
                double angle = d * 3.14159265358979323846 / 4.0;
                global_wps.push_back({nfz.cx + R * cos(angle), nfz.cy + R * sin(angle)});
            }
        } else {
            global_wps.push_back({nfz.x1 - margin, nfz.y1 - margin});
            global_wps.push_back({nfz.x1 - margin, nfz.y2 + margin});
            global_wps.push_back({nfz.x2 + margin, nfz.y1 - margin});
            global_wps.push_back({nfz.x2 + margin, nfz.y2 + margin});
        }
    }
    
    precompute_static_edges(nfzs);

    vector<Point> charging_stations;
    Json::Value cs_list = input_data.get("charging_stations", Json::Value(Json::arrayValue));
    for (const auto &cs : cs_list) {
        charging_stations.push_back(Point{cs["x"].asDouble(), cs["y"].asDouble()});
    }

    // ==================== SCHEDULING ====================
    Json::Value flight_manifest(Json::arrayValue);
    int num_drones = (int)drones.size();

    vector<vector<Json::Value>> drone_trip_paths(num_drones);
    vector<double> drone_times(num_drones, 0.0);

    vector<int> remaining;
    for (int i = 0; i < (int)deliveries.size(); ++i) {
        bool any = false;
        for (const auto &dr : drones) {
            if (deliveries[i].weight <= dr.max_payload + EPS) {
                any = true; break;
            }
        }
        if (any) remaining.push_back(i);
    }

    while (!remaining.empty()) {
        int best_drone = 0;
        for (int d = 1; d < num_drones; d++) {
            if (drone_times[d] < drone_times[best_drone]) best_drone = d;
        }

        if (drone_times[best_drone] >= 1e18) {
            break; // All drones are retired
        }

        vector<int> trip = build_trip(remaining, deliveries, drones[best_drone],
            warehouse, charging_stations, nfzs, drone_times[best_drone]);

        if (trip.empty()) {
            drone_times[best_drone] = 1e18; // retire this drone
            continue;
        }

        TripResult res = simulate_trip(trip, deliveries, warehouse,
            charging_stations, nfzs, drone_times[best_drone]);

        if (!res.success || res.delivered.empty()) {
            // Should theoretically never happen since build_trip validates
            drone_times[best_drone] = 1e18;
            continue;
        }

        drone_trip_paths[best_drone].push_back(res.path);
        drone_times[best_drone] = res.end_time;

        vector<int> filtered;
        for (int idx : remaining) {
            if (find(res.delivered.begin(), res.delivered.end(), idx) == res.delivered.end()) {
                filtered.push_back(idx);
            }
        }
        remaining.swap(filtered);
    }

    for (int di = 0; di < num_drones; di++) {
        for (const auto &trip_path : drone_trip_paths[di]) {
            if (trip_path.empty()) continue;
            Json::Value drone_entry;
            drone_entry["drone_id"] = drones[di].id;
            drone_entry["path"] = trip_path;
            flight_manifest.append(drone_entry);
        }
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
