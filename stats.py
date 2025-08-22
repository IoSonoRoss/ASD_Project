import time

class StatsTracker:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.execution_time = 0
        self.frontier_cells_discovered = set()
        self.pruning_success_count = 0
        self.recursion_depth = 0

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()
        self.execution_time = self.end_time - self.start_time

    def add_frontier_cells(self, frontier_cells):
        coords = {item[0] for item, _ in frontier_cells}
        self.frontier_cells_discovered.update(coords)

    def increment_pruning_count(self):
        self.pruning_success_count += 1
    
    def track_depth(self, depth):
        if depth > self.recursion_depth:
            self.recursion_depth = depth
        
    def get_summary(self):
        return {
            "execution_time": self.execution_time,
            "total_unique_frontiers": len(self.frontier_cells_discovered),
            "pruning_successes": self.pruning_success_count,
            "max_recursion_depth": self.recursion_depth + 1 # +1 perché depth parte da 0
        }