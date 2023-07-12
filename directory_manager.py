import os


class DirectoryManager:
    def __init__(self, image_path, base_path):
        self.image_path = image_path
        self.base_path = base_path
        self.output_path = None
        self.initialize_output_path()

    # Initialize the output path based on the image name
    def initialize_output_path(self):

        image_name = os.path.basename(self.image_path)
        image_name_without_extension = os.path.splitext(image_name)[0]

        self.output_path = os.path.join(self.base_path, f'output-{image_name_without_extension}')

    # Return the output path
    def get_output_path(self):
        return self.output_path

    # Create a new directory for images
    def create_images_folder(self):

        full_path = os.path.join(self.output_path, 'images')

        if not os.path.exists(full_path):
            os.makedirs(full_path)

        return full_path

    # Create output folders for each row
    def create_output_folder_rows(self, rows_position):

        output_paths_graphs = []

        for i in range(len(rows_position)):
            full_path = os.path.join(self.output_path, 'row-' + str(i + 1))
            output_paths_graphs.append(full_path)

            if not os.path.exists(full_path):
                os.makedirs(full_path)

        return output_paths_graphs
