class LRUPageFaultSimulator:
    def __init__(self, capacity):
        self.capacity = capacity
        self.page_frames = []
        self.page_order = []
        self.page_faults = 0
        self.page_hits = 0

    def apply_lru_algorithm(self,page):
        lru_page = self.page_order.pop(0)
        self.page_frames.remove(lru_page)
        self.page_frames.append(page)

    def simulate_page_fault(self, page):
        if page in self.page_frames:
            self.page_hits += 1
            self.page_order.remove(page)
            self.page_order.append(page)
            print(f"Page hit for page {page}. Page frames unchanged.")
        else:
            self.page_faults += 1
            if len(self.page_frames) < self.capacity:
                self.page_frames.append(page)
            else:
                self.apply_lru_algorithm(page)
            self.page_order.append(page)
            print(f"Page fault for page {page}. Page frames after fault: {self.page_frames}")

    def run_simulation(self, pages):
        for page in pages:
            self.simulate_page_fault(page)
        print(f"\nTotal page faults: {self.page_faults}")
        print(f"Total page hits: {self.page_hits}")


# Contoh penggunaan
if __name__ == "__main__":
    capacity = int(input("Enter the number of page frames: "))
    page_sequence = input("Enter the page sequence (space-separated): ").split()
    simulator = LRUPageFaultSimulator(capacity)
    simulator.run_simulation(page_sequence)
