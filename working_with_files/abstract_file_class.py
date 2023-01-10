from abc import abstractmethod, ABC
import pandas as pd
import os


def check_if_file_exists() -> tuple:
    """Function that checks if user input is correct. And if it is it allows the program to proceed with the
    analysis."""

    while True:
        file_path = input("Input File path: ")
        file_name = input("Input File name: ")
        full_path = os.path.join(file_path, file_name)
        if os.path.exists(full_path):
            return file_path, file_name
        else:
            print("No such file. Try again.")


class InputFile(ABC):

    list_of_norms = []

    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name

    @abstractmethod
    def connect_to_a_file_and_read_content(self):
        """An example of overload. Method that every instance needs to have in order to read files properly.
        Files with norms and without norms do not contain teh same columns, so method need to be overwritten."""

        pass

    @staticmethod
    def group_and_sum_data_level0(data: pd.DataFrame) -> pd.DataFrame:
        """Method that groups data based on code level 0, if needed it is going to be used for visualisation"""

        report = data.groupby("Уровень 0", as_index=False)[["Всего человеко часов",
                                                            "Всего машино часов",
                                                            "ОБЪЕМ – Y.0"]].sum()
        print(report)
        return report

    @staticmethod
    def group_and_sum_data_level1(data: pd.DataFrame) -> pd.DataFrame:
        """Method that groups data based on code level 1, if needed it is going to be used for visualisation"""
        report = data.groupby("Уровень 1", as_index=False)[["Всего человеко часов",
                                                            "Всего машино часов",
                                                            "ОБЪЕМ – Y.1"]].sum()
        print(report)
        return report

    @staticmethod
    def group_and_sum_data_level2(data: pd.DataFrame) -> pd.DataFrame:
        """Method that groups data based on code level 2, if needed it is going to be used for visualisation"""
        report = data.groupby("Уровень 2", as_index=False)[["Всего человеко часов",
                                                            "Всего машино часов",
                                                            "ОБЪЕМ – Y.2"]].sum()
        print(report)
        return report

    @staticmethod
    def group_and_sum_data_level3(data: pd.DataFrame) -> pd.DataFrame:
        """Method that groups data based on code level 3, if needed it is going to be used for visualisation"""
        report = data.groupby("Уровень 3", as_index=False)[["Всего человеко часов",
                                                            "Всего машино часов",
                                                            "ОБЪЕМ 1 – Y.3"]].sum()
        print(report)
        return report

    @staticmethod
    def group_and_sum_data_level4(data: pd.DataFrame) -> pd.DataFrame:
        """Method that groups data based on code level 4, if needed it is going to be used for visualisation, but the
        main goal for this method is to allow easier manipulation whilst defining average norms i recomputing total
        hours."""

        report = data.groupby("Уровень 4", as_index=False)[["Всего человеко часов", "Всего машино часов",
                                                            "ОБЪЕМ 1 - У.4", "ОБЪЕМ 2 - У.4", "ОБЪЕМ 3 - У.4"]].sum()

        return report

    def connect_to_a_file_and_read_content_codes(self) -> pd.DataFrame:
        """Method that connects to a file that contains data for codes like unit measures."""
        try:
            columns = ["Позиции дла Контрактации", "Наименование позиции", "1. Ед.изм.", "2. Ед.изм.", "3. Ед.изм."]
            path = os.path.join(self.file_path, "TP.xlsx")
            file_input = pd.read_excel(path)
            data_for_codes = pd.DataFrame(file_input, columns=columns)
            return data_for_codes
        except FileNotFoundError:
            print("No such File in the directory.")

    def create_a_file_with_average_norms(self) -> pd.DataFrame:
        """Method that writes average norms in the Excel file"""

        list_data_frame = []

        try:
            for code in self.list_of_norms:
                list_data_frame.append(code.__dict__)
            data = pd.DataFrame(list_data_frame)
            data_avg_norms = data[["name_level4", "description_level4", "unit_measure_l4_1", "avg_labor_1", "avg_mach_1"]]

            data_avg_norms.to_excel("Average norms.xlsx", sheet_name="Average norms", float_format="%.10f", index=False)
            print("If created, average norms are stored in the Average norms.xlsx file")
            return data_avg_norms
        except PermissionError:
            print("File you are trying to write in is already open. Close the file and try again.")
        except KeyError:
            print("Column Уровень 4, could not be found.")
