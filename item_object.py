class itemObj:
    def __init__(self, item_name):
        self.item_name = item_name
        self.group_list = []
        self.len_group_list = 0
        self.total_size = 0
        self.group_size = {}
        self.addr_code = 0
        self.addr_data = 0
        self.addr_reserved = 0
        self.addr_free = 0
        self.addr_total = 0
        self.total_size = 0

    def _insert_summary(self, code, data, reserved, free, total):
        self.addr_code = code
        self.addr_data = data
        self.addr_reserved = reserved
        self.addr_free = free
        self.addr_total = total

    def _insert_gap_info(self, free, sum_gap, min_gap, max_gap):
        self.free = free
        self.sum_gap = sum_gap
        self.min_gap = min_gap
        self.max_gap = max_gap
        # print(f'[{self.item_name}] free, sum_gap, min_gap, max_gap :{self.free, self.sum_gap, self.min_gap, self.max_gap}')

    def _insert_group_info(self, group, section, size, space_addr, chip_addr, alignment):
        # if group in self.group_list:
        self.group_list.append(
            [group, section, size, space_addr, chip_addr, alignment])
        self.total_size += int(size, 16)
        self.len_group_list = len(self.group_list)

    def exist_group_info(self, group):
        for i in range(self.len_group_list):
            inserted_group_name = self.group_list[i]
            if group in inserted_group_name:
                #print(f'found same group : {inserted_group_name}')
                return True

        return False

    def add_size(self, exist_size, new_size):
        # print(f'exist_size : {exist_size}')
        # print(f'new_size : {new_size}')
        size_1 = int(exist_size, 16)
        size_2 = int(new_size, 16)

        return hex(size_1 + size_2)

    def calculate_group_size(self):
        total = 0
        keys = list(self.group_size.keys())
        values = list(self.group_size.values())
        # print(values)
        for i in range(len(values)):
            size = int(values[i], 16)
            total += size
        self.total_size = total

        return total
        #print(f'total : {total}')
