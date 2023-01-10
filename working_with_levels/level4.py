class Level4:
    def __init__(self, name_level4, description_level4, unit_measure_l4_1, avg_labor_1, avg_mach_1,
                 unit_measure_l4_2, unit_measure_l4_3, avg_labor_2=0, avg_mach_2=0, avg_labor_3=0, avg_mach_3=0):
        self.name_level4: str = name_level4
        self.description_level4: str = description_level4
        self.unit_measure_l4_1: str = unit_measure_l4_1
        self.avg_labor_1: float = avg_labor_1
        self.avg_mach_1: float = avg_mach_1
        self.unit_measure_l4_2: str = unit_measure_l4_2
        self.avg_labor_2: float = avg_labor_2
        self.avg_mach_2: float = avg_mach_2
        self.unit_measure_l4_3: str = unit_measure_l4_3
        self.avg_labor_3: float = avg_labor_3
        self.avg_mach_3: float = avg_mach_3

    def __str__(self):
        return f"\nLevel 4: {self.name_level4}\nDescription: {self.description_level4}\n" \
               f"Average labor hours based on the first measure: {round(self.avg_labor_1, 4)} " \
               f"{self.unit_measure_l4_1}\n" \
               f"Average machine hours based on the first measure: {round(self.avg_mach_1, 4)} " \
               f"{self.unit_measure_l4_1}\n" \
               f"Average machine hours based on the second measure: {round(self.avg_labor_2, 4)} " \
               f"{self.unit_measure_l4_2}\n" \
               f"Average machine hours based on the second measure: {round(self.avg_mach_2, 4)} " \
               f"{self.unit_measure_l4_2}\n" \
               f"Average machine hours based on the third measure: {round(self.avg_labor_3, 4)} " \
               f"{self.unit_measure_l4_3}\n" \
               f"Average machine hours based on the third measure: {round(self.avg_mach_3, 4)} " \
               f"{self.unit_measure_l4_3}\n{'-'*40}"

    def __repr__(self):
        return f"\nLevel 4: {self.name_level4}\nDescription: {self.description_level4}\n" \
               f"Average labor hours based on the first measure: {round(self.avg_labor_1, 4)} " \
               f"{self.unit_measure_l4_1}\n" \
               f"Average machine hours based on the first measure: {round(self.avg_mach_1, 4)} " \
               f"{self.unit_measure_l4_1}\n{'-'*40}"



