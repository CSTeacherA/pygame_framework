import pygame
import sys

def is_two_surfaces_equal(surface1: pygame.Surface, surface2: pygame.Surface):
    # Check if dimensions and format are the same
    if surface1.get_size() != surface2.get_size() or surface1.get_bitsize() != surface2.get_bitsize():
        return False
    # Compare raw pixel data
    return surface1.get_view().raw == surface2.get_view().raw

def calculate_grid_size(image, cell_width, cell_height):
    return (image.get_width() // cell_width, image.get_height() // cell_height)

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)