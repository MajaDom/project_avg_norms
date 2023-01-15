import math
from working_with_files.abstract_file_class import InputFile
import os
import pandas as pd
from working_with_levels.level4 import Level4


class FileWithNorms(InputFile):

    def __init__(self, file_path, file_name):
        """Method that initializes object File, based on the user input. File contains norms."""
        super().__init__(file_path, file_name)

    def __str__(self):
        return f"File path: {self.file_path}\nFile name: {self.file_name}"

    def connect_to_a_file_and_read_content(self) -> pd.DataFrame:
        """Method that that connects to Excel file and loads the data."""

        columns = ["Наименование объекта", "Наименование раздела", "Шифра раздела", "Тип раздела",
                   "Уникальный номер - Работа", "V", "ВР", "Кол-во", "Е.И.", "Всего человеко часов",
                   "Всего машино часов", "Уровень 4", "Наименование У.4", "ОБЪЕМ 1 - У.4", "Ед. Изм. 1 (У.4)",
                   "ОБЪЕМ 2 - У.4", "Ед. Изм. 2 (У.4)", "ОБЪЕМ 3 - У.4", "Ед. Изм. 3 (У.4)", "Уровень 3",
                   "Наименование Y.3", "ОБЪЕМ 1 – Y.3", "Ед. изм. 1 Y.3", "ОБЪЕМ 2 – Y.3", "Ед. изм. 2 Y.3",
                   "ОБЪЕМ 3 – Y.3", "Ед. изм. 3 Y.3", "Уровень 2", "Наименование Y.2", "ОБЪЕМ – Y.2", "Ед. изм. Y.2",
                   "Уровень 1", "Наименование Y.1", "ОБЪЕМ – Y.1", "Ед. изм. Y.1", "Уровень 0", "Наименование Y.0",
                   "ОБЪЕМ – Y.0", "Ед. изм. Y.0"]

        try:
            path = os.path.join(self.file_path, self.file_name)
            file_input = pd.read_excel(path)
            data_for_report = pd.DataFrame(file_input, columns=columns)
            print("File is loaded, we will proceed with creating average norms.")
            return data_for_report
        except FileNotFoundError:
            print("No such file in the directory.")

    def create_average_hours_level4(self, grouped_data: pd.DataFrame) -> pd.DataFrame:
        """Method that calculates average norms based on quantity1 (the reason for using that quantity is because
        every code must have at least that one)."""

        data_code = self.connect_to_a_file_and_read_content_codes()
        grouped_data["Среднаяя норма - чел.ч. Объем 1"] = grouped_data["Всего человеко часов"] / grouped_data[
            "ОБЪЕМ 1 - У.4"]
        grouped_data["Среднаяя норма - маш.ч. Объем 1"] = grouped_data["Всего машино часов"] / grouped_data[
            "ОБЪЕМ 1 - У.4"]
        grouped_data["Среднаяя норма - чел.ч. Объем 2"] = grouped_data["Всего человеко часов"] / grouped_data[
            "ОБЪЕМ 2 - У.4"]
        grouped_data["Среднаяя норма - маш.ч. Объем 2"] = grouped_data["Всего машино часов"] / grouped_data[
            "ОБЪЕМ 2 - У.4"]
        grouped_data["Среднаяя норма - чел.ч. Объем 3"] = grouped_data["Всего человеко часов"] / grouped_data[
            "ОБЪЕМ 3 - У.4"]
        grouped_data["Среднаяя норма - маш.ч. Объем 3"] = grouped_data["Всего машино часов"] / grouped_data[
            "ОБЪЕМ 3 - У.4"]
        data_merged = grouped_data.merge(data_code, left_on="Уровень 4", right_on="Позиции дла Контрактации")
        return data_merged

    @staticmethod
    def fill_level4_avg_norms(grouped_data: pd.DataFrame) -> list[Level4]:
        """Method that creates object Level 4 for every average norm"""

        data = grouped_data.itertuples(index=False, name=None)
        codes = []
        for code in data:
            codes.append(Level4(name_level4=code[0], description_level4=code[13], unit_measure_l4_1=code[14],
                                avg_labor_1=code[6], avg_mach_1=code[7], unit_measure_l4_2=code[15],
                                avg_labor_2=code[8], avg_mach_2=code[9], unit_measure_l4_3=code[16],
                                avg_labor_3=code[10], avg_mach_3=code[11]))
        return codes

    @staticmethod
    def find_missing_norms(codes: list[Level4]) -> list[Level4]:
        """Function that finds codes with no average norms and stores it in a list. When quantity1 is equal to 0,
        there is no way we can get average norm, so with this method we find such codes and store them for later
        manipulation."""

        list_of_missing_norms = []
        for item in codes:
            if math.isinf(item.avg_labor_1):
                list_of_missing_norms.append(item)
        return list_of_missing_norms

    def store_calculated_norms(self, codes: list[Level4]) -> list[Level4]:
        """Method that appends list with calculated average norms"""
        for item in codes:
            if math.isinf(item.avg_labor_1) is not True:
                self.list_of_norms.append(item)
        return self.list_of_norms

    def input_missing_norms_console(self, text, missing_norms: list) -> list:
        """Method that allows user to input missing norms through the console.
        If there are total hours but the quantity1 is equal to 0, that is a mistake in the norming process.
        In those cases, this method allows the user to input average norms."""

        print(f"Number of missing norms is {len(missing_norms)}.")
        if text == "console":
            for code in missing_norms:
                print(f"Level 4: {code.name_level4} Measure: {code.unit_measure_l4_1}")
                code.avg_labor_1 = self.test_user_input_float_hours("labor")
                code.avg_mach_1 = self.test_user_input_float_hours("machine")
                self.list_of_norms.append(code)
            return self.list_of_norms

    def start_the_program_and_create_avg_norms(self, base_data) -> pd.DataFrame:
        """Method that combines all methods and completes first stage of analysis. The end result is a file that
        contains all average norms based on the firs input file that contains total hours gained by the norming process
        and not average norms."""
        try:
            grouped_data = self.group_and_sum_data_level4(base_data)
            calculate_avg_norms = self.create_average_hours_level4(grouped_data)
            codes_level4 = self.fill_level4_avg_norms(calculate_avg_norms)
            self.store_calculated_norms(codes_level4)
            missing_norms = self.find_missing_norms(codes_level4)
            self.input_missing_norms_console("console", missing_norms)
            average_norms = self.create_a_file_with_average_norms()
            return average_norms
        except ValueError:
            print("Can't merge files containing code data and total hours.")
        except KeyError:
            print("Missing columns.")
