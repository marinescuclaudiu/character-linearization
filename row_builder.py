import os
from box import Box


class RowBuilder:

    def __init__(self):
        self.boxes = []
        self.rows = []

    def read_boxes(self, input_path):

        with open(input_path, encoding='utf8') as file:

            for i, line in enumerate(file):
                values = line.strip().split()

                top_left_x = float(values[0])
                top_left_y = float(values[1])
                bot_right_x = float(values[2])
                bot_right_y = float(values[3])
                label = values[4]

                box = Box(i, top_left_x, top_left_y, bot_right_x, bot_right_y, label, None)

                self.boxes.append(box)

    def create_rows(self, rows_position):

        for i in range(len(rows_position)):
            self.rows.append([])

        return

    def distribute_boxes_to_rows_by_attraction(self, rows_position, w1=0.99, threshold=3.96):

        if len(rows_position) == 1:

            for box in self.boxes:
                self.rows[0].append(box)

            return

        w2 = 1 - w1

        for box in self.boxes:

            if box.y_center <= rows_position[0]:
                self.rows[0].append(box)
                continue

            if box.y_center > rows_position[-1]:
                self.rows[-1].append(box)
                continue

            for i in range(0, len(rows_position) - 1):

                row_above = rows_position[i]
                row_below = rows_position[i + 1]

                if box.y_center == row_below:
                    self.rows[i+1].append(box)
                    break

                if row_above < box.y_center < row_below:

                    f_above = (w1 * w2) / ((box.y_center - row_above) ** 2)

                    f_below = w1 / (w2 * ((box.y_center - row_below) ** 2))

                    if f_below < threshold <= f_above:
                        self.rows[i].append(box)

                    if f_above < threshold <= f_below:
                        self.rows[i+1].append(box)

                    break

    def distribute_boxes_to_rows_by_position(self, rows_position):

        if len(rows_position) == 1:

            for box in self.boxes:
                self.rows[0].append(box)

            return

        for box in self.boxes:

            if box.y_center <= rows_position[0]:
                self.rows[0].append(box)
                continue

            if box.y_center > rows_position[-1]:
                self.rows[-1].append(box)
                continue

            for i in range(len(rows_position) - 1):
                row_above = rows_position[i]
                row_below = rows_position[i+1]

                if row_above < box.y_center <= row_below:

                    if box.y_center - row_above < row_below - box.y_center:
                        self.rows[i].append(box)
                    else:
                        self.rows[i+1].append(box)

                    break

    def sort_rows(self):

        for i in range(len(self.rows)):
            self.rows[i].sort(key=lambda box: box.x_center)

    def group_and_arrange_boxes(self, row):

        visited = set()
        arrangement = []

        for i in range(len(row) - 1):
            box = row[i]
            next_box = row[i + 1]
            if box.is_overlapping(next_box):
                arrangement.append([box, next_box])
                visited.add(box)
                visited.add(next_box)

            else:
                if box not in visited:
                    arrangement.append(box)
                    visited.add(box)

        if row[-1] not in visited:
            arrangement.append(row[-1])

        result = []
        i = 0
        last_visited = False

        while i < len(arrangement)-1:
            if isinstance(arrangement[i], list) and isinstance(arrangement[i+1], list) and arrangement[i][1] == arrangement[i+1][0]:
                result.append(arrangement[i][0])
                result.append(arrangement[i][1])
                result.append(arrangement[i+1][1])
                if i == len(arrangement) - 2:
                    last_visited = True
                i += 2
            else:
                result.append(arrangement[i])
                i += 1

        if not last_visited:
            result.append(arrangement[-1])

        return result

    def write_rows(self, output_path):

        output_path = os.path.join(output_path, 'transcriere.txt')

        with open(output_path, 'w', encoding='utf-8') as file:
            for row in self.rows:
                for element in row:
                    if isinstance(element, list):
                        file.write(f"[{element[0].label}|{element[1].label}]")
                    else:
                        file.write(element.label)
                file.write('\n')

    def build_rows(self, rows_position):

        self.create_rows(rows_position)

        self.distribute_boxes_to_rows_by_position(rows_position)

        self.sort_rows()

        for i in range(len(self.rows)):
            self.rows[i] = self.group_and_arrange_boxes(self.rows[i])

        return self.rows
