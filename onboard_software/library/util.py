import math

class Util:

    # Conversion constants
    MM_PER_INCH = 25.4
    METERS_PER_INCH = MM_PER_INCH / 1000.0
    INCHES_PER_MM = 1.0 / MM_PER_INCH
    INCHES_PER_CM = 10.0 / MM_PER_INCH
    INCHES_PER_METER = 1000.0 / MM_PER_INCH
    
    @staticmethod
    def clip(value, min_value, max_value):
        """
        Clips the input value to be within [min_value, max_value].
        """
        return max(min_value, min(value, max_value))
    
    @staticmethod
    def magnitude(*nums):
        """
        Calculate the magnitude of a given set of numbers.
        """
        total = 0.0
        for num in nums:
            total += num * num
        return math.sqrt(total)
    
    @staticmethod
    def signum(x):
        """
        Returns the sign of the given number.
        """
        return (x > 0) - (x < 0)