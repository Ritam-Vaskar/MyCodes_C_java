// Start of HEAD
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <unordered_set>
#include <sstream>
#include <algorithm>

using namespace std;

struct User {
	string name;
	int budget;
	int energy;
	set<string> tags;
	bool active = true;
};

struct Activity {
	int id;
	string name;
	int cost;
	int duration;
	int energy;
	string tag;
};

struct Input {
	int N, D, H;
	vector<User> users;
	map<int, Activity> activities;     // ordered by id
	vector<string> events;             // verbatim event lines
};

static Input readInput() {
	Input in;
	cin >> in.N >> in.D >> in.H;
	in.users.resize(in.N);
	for (int i = 0; i < in.N; i++) {
		int k;
		cin >> in.users[i].name >> in.users[i].budget >> in.users[i].energy >> k;
		for (int j = 0; j < k; j++) {
			string t; cin >> t;
			in.users[i].tags.insert(t);
		}
		in.users[i].active = true;
	}
	int A; cin >> A;
	for (int i = 0; i < A; i++) {
		Activity a;
		cin >> a.id >> a.name >> a.cost >> a.duration >> a.energy >> a.tag;
		in.activities[a.id] = a;
	}
	int E; cin >> E;
	cin.ignore();
	for (int i = 0; i < E; i++) {
		string line;
		getline(cin, line);
		while (!line.empty() && (line.back() == '\r' || line.back() == ' ')) line.pop_back();
		in.events.push_back(line);
	}
	return in;
}

/** Format a single day line exactly per spec. Use REST if ids is empty. */
static string formatDay(int day, vector<int> ids, int cost, int sat) {
	if (ids.empty()) {
		return "Day " + to_string(day) + ": REST | cost=0 satisfaction=0";
	}
	sort(ids.begin(), ids.end());
	string s = "Day " + to_string(day) + ": ";
	for (size_t i = 0; i < ids.size(); i++) {
		if (i) s += ' ';
		s += to_string(ids[i]);
	}
	s += " | cost=" + to_string(cost) + " satisfaction=" + to_string(sat);
	return s;
}

// End of HEAD

// Start of BODY

struct DayPlan {
	vector<int> ids;
	int cost = 0;
	int sat = 0;
};

static int activeCount(const vector<User> &users) {
	int cnt = 0;
	for (const auto &u : users) if (u.active) cnt++;
	return cnt;
}

static int minBudget(const vector<User> &users) {
	int best = -1;
	for (const auto &u : users) {
		if (!u.active) continue;
		if (best == -1 || u.budget < best) best = u.budget;
	}
	return best;
}

static int minEnergy(const vector<User> &users) {
	int best = -1;
	for (const auto &u : users) {
		if (!u.active) continue;
		if (best == -1 || u.energy < best) best = u.energy;
	}
	return best;
}

static int tagLikeCount(const vector<User> &users, const string &tag) {
	int cnt = 0;
	for (const auto &u : users) {
		if (!u.active) continue;
		if (u.tags.count(tag)) cnt++;
	}
	return cnt;
}

static DayPlan chooseBestDayPlan(const map<int, Activity> &activities,
								const vector<User> &users,
								const unordered_set<string> &blocked,
								const unordered_set<int> &used,
								int H) {
	DayPlan best;
	if (activeCount(users) == 0) {
		return best;
	}

	int budget_limit = minBudget(users);
	int energy_limit = minEnergy(users);
	if (budget_limit < 0 || energy_limit < 0) {
		return best;
	}

	vector<Activity> eligible;
	for (const auto &kv : activities) {
		const Activity &a = kv.second;
		if (used.count(a.id)) continue;
		if (blocked.count(a.tag)) continue;
		eligible.push_back(a);
	}

	int n = (int)eligible.size();
	vector<int> likeCount(n, 0);
	for (int i = 0; i < n; i++) {
		likeCount[i] = tagLikeCount(users, eligible[i].tag);
	}

	int bestSat = -1;
	int bestCost = 0;
	vector<int> bestIds;

	if (n >= 63) {
		return best;
	}
	size_t totalMasks = 1ULL << n;
	for (size_t mask = 0; mask < totalMasks; mask++) {
		int cost = 0;
		int duration = 0;
		int energy = 0;
		int sat = 0;
		vector<int> ids;

		for (int i = 0; i < n; i++) {
			if (mask & (1ULL << i)) {
				cost += eligible[i].cost;
				duration += eligible[i].duration;
				energy += eligible[i].energy;
				sat += likeCount[i];
				ids.push_back(eligible[i].id);
			}
		}

		if (cost > budget_limit || energy > energy_limit || duration > H) {
			continue;
		}
		sort(ids.begin(), ids.end());

		bool better = false;
		if (sat > bestSat) {
			better = true;
		} else if (sat == bestSat) {
			if (cost < bestCost) {
				better = true;
			} else if (cost == bestCost) {
				if (lexicographical_compare(ids.begin(), ids.end(), bestIds.begin(), bestIds.end())) {
					better = true;
				}
			}
		}

		if (better) {
			bestSat = sat;
			bestCost = cost;
			bestIds = ids;
		}
	}

	if (bestIds.empty()) {
		return best;
	}
	best.ids = bestIds;
	best.cost = bestCost;
	best.sat = bestSat;
	return best;
}

static void buildPlanFrom(int startDay,
						  const Input &in,
						  const vector<User> &users,
						  const vector<unordered_set<string>> &blockedByDay,
						  vector<DayPlan> &plan) {
	if (startDay < 1) startDay = 1;
	if (startDay > in.D) return;
	unordered_set<int> used;
	for (int day = 1; day < startDay; day++) {
		for (int id : plan[day].ids) used.insert(id);
	}

	for (int day = startDay; day <= in.D; day++) {
		DayPlan dp = chooseBestDayPlan(in.activities, users, blockedByDay[day], used, in.H);
		plan[day] = dp;
		for (int id : dp.ids) used.insert(id);
	}
}

static void applyEvent(const string &line,
					   vector<User> &users,
					   const map<string, int> &userIndex,
					   vector<unordered_set<string>> &blockedByDay,
					   int &eventDay) {
	stringstream ss(line);
	string type;
	if (!(ss >> type >> eventDay)) {
		return;
	}
	if (eventDay < 1 || eventDay >= (int)blockedByDay.size()) {
		return;
	}
	if (type == "WEATHER") {
		string tag;
		ss >> tag;
		if (eventDay >= 1 && eventDay < (int)blockedByDay.size()) {
			blockedByDay[eventDay].insert(tag);
		}
		return;
	}
	string name;
	ss >> name;
	auto it = userIndex.find(name);
	if (it == userIndex.end()) {
		return;
	}
	int idx = it->second;

	if (type == "DROP") {
		users[idx].active = false;
	} else if (type == "FATIGUE") {
		int val;
		ss >> val;
		users[idx].energy = val;
	} else if (type == "BUDGET") {
		int val;
		ss >> val;
		users[idx].budget = val;
	}
}

static string solve(Input in) {
	string out;

	map<string, int> userIndex;
	for (int i = 0; i < (int)in.users.size(); i++) {
		userIndex[in.users[i].name] = i;
	}

	vector<unordered_set<string>> blockedByDay(in.D + 1);
	vector<DayPlan> plan(in.D + 1);

	buildPlanFrom(1, in, in.users, blockedByDay, plan);

	out += "=== PLAN ===\n";
	for (int day = 1; day <= in.D; day++) {
		out += formatDay(day, plan[day].ids, plan[day].cost, plan[day].sat) + "\n";
	}

	for (size_t i = 0; i < in.events.size(); i++) {
		const string &line = in.events[i];
		int eventDay = 1;
		applyEvent(line, in.users, userIndex, blockedByDay, eventDay);

		buildPlanFrom(eventDay, in, in.users, blockedByDay, plan);

		out += "=== EVENT " + to_string(i + 1) + ": " + line + " ===\n";
		for (int day = eventDay; day <= in.D; day++) {
			out += formatDay(day, plan[day].ids, plan[day].cost, plan[day].sat) + "\n";
		}
	}

	return out;
}

int main() {
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	Input in = readInput();
	cout << solve(in);
	return 0;
}

// End of BODY

// Start of TAIL
// End of TAIL
