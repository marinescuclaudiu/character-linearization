import argparse
from directory_manager import DirectoryManager
from row_finder import RowFinder
from row_builder import RowBuilder
from graph_builder import GraphBuilder


def start_algorithm(image_path, boxes_path, output_path):
    directory_manager = DirectoryManager(image_path, output_path)

    row_finder = RowFinder()

    output_path_images = directory_manager.create_images_folder()

    row_finder.set_output_path(output_path_images)

    row_finder.read_image(image_path)

    peaks = row_finder.find_rows()

    row_builder = RowBuilder()

    row_builder.read_boxes(boxes_path)

    rows = row_builder.build_rows(peaks)

    output_path_transcription = directory_manager.get_output_path()

    row_builder.write_rows(output_path_transcription)

    output_path_graphs = directory_manager.create_output_folder_rows(peaks)

    graph_builder = GraphBuilder()

    for i in range(len(rows)):
        graph_builder.build_graph(rows[i])
        graph_builder.save_graph(output_path_graphs[i])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start the algorithm.')
    parser.add_argument('image_path', type=str, help='The path to the image file')
    parser.add_argument('boxes_path', type=str, help='The path to the boxes file')
    parser.add_argument('output_path', type=str, help='The path where output should be saved')
    args = parser.parse_args()
    start_algorithm(args.image_path, args.boxes_path, args.output_path)

