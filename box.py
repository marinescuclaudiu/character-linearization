class Box:
    def __init__(self, id, top_left_x, top_left_y, bot_right_x, bot_right_y, label, line_above):
        self.id = id
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bot_right_x = bot_right_x
        self.bot_right_y = bot_right_y
        self.x_center = (top_left_x + bot_right_x) / 2
        self.y_center = (top_left_y + bot_right_y) / 2
        self.label = label
        self.line_above = line_above

    # Determine if this box is overlapping with another box
    def is_overlapping(self, other):

        # Calculate the horizontal overlap
        overlap = other.top_left_x - self.bot_right_x

        # There is no overlap
        if overlap >= 0:
            return False

        # If the overlap is greater or equal to half the width of this box, then the boxes are overlapping
        if abs(overlap) >= (self.bot_right_x - self.top_left_x) / 2:
            return True

        # There is overlap, but it is not significant, so the boxes are not overlapping
        return False
