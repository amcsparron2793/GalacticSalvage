class ColorConverter:
    """
    This module provides a color conversion utility class, `ColorConverter`, which contains static methods for converting colors between different representations.

    """
    @staticmethod
    def rgb_to_hex(rgb):
        """
        Convert RGB tuple to hexadecimal color representation.

        Args:
            rgb (tuple): RGB color tuple in the format (R, G, B) where each component is an integer between 0 and 255.

        Returns:
            str: Hexadecimal color representation.
        """
        return '#{0:02x}{1:02x}{2:02x}'.format(*rgb)

    @staticmethod
    def hex_to_rgb(hex_color):
        """
        Convert hexadecimal color representation to RGB tuple.

        Args:
            hex_color (str): Hexadecimal color representation (e.g., '#RRGGBB').

        Returns:
            tuple: RGB color tuple in the format (R, G, B) where each component is an integer between 0 and 255.
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
