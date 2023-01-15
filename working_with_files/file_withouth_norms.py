from working_with_files.abstract_file_class import InputFile
import os
import pandas as pd
import math
from working_with_levels.level4 import Level4
from working_with_visualisations.visualisation import show_lab_hours, show_mach_hours


class FileWithoutNorms(InputFile):

    def __init__(self, file_path, file_name):
        """Method that initializes object File, based on the user input."""
        super().__init__(file_path, file_name)

    def __str__(self):
        return f"File name: {self.file_path}\nFile path: {self.file_name}"

    def connect_to_a_file_and_read_content(self) -> pd.DataFrame:
        """Method that that connects to Excel file and loads the data."""

        columns = ["Наименование объекта", "Наименование подобъекта", "Шифр подобъекта", "Раздел", "Уникальный номер",
                   "Ведущая позиция", "Проектное наименование материала/ Описание работы", "Уровень 4", "ОБЪЕМ 1 - У.4",
                   "ОБЪЕМ 2 - У.4", "ОБЪЕМ 3 - У.4", "Уровень 3", "ОБЪЕМ 1 – Y.3", "ОБЪЕМ 2 – Y.3", "ОБЪЕМ 3 – Y.3",
                   "Уровень 2", "ОБЪЕМ – Y.2", "Уровень 1", "ОБЪЕМ – Y.1", "Уровень 0", "ОБЪЕМ – Y.0"]
        try:
            path = os.path.join(self.file_path, self.file_name)
            file_input = pd.read_excel(path)
            data_for_report = pd.DataFrame(file_input, columns=columns)
            print(data_for_report)
            return data_for_report
        except FileNotFoundError:
            print("No such file in the directory.")

    def calculate_total_avg_hours_rev1(self, data: pd.DataFrame) -> pd.DataFrame:
        """Method that computes total hours based on previously calculated average norms.
        It returns a DataFrame with every position and its corresponding total hours."""

        path_to_avg_norm = os.path.join(self.file_path, "Average norms.xlsx")
        file_input_avg_norms = pd.read_excel(path_to_avg_norm)
        data_avg_norms = pd.DataFrame(file_input_avg_norms, columns=["name_level4", "avg_labor_1", "avg_mach_1"])

        compare_data_frame = data.merge(data_avg_norms, how="left", left_on="Уровень 4", right_on="name_level4")
        compare_data_frame["Всего человеко часов"] = compare_data_frame["ОБЪЕМ 1 - У.4"] * compare_data_frame[
            "avg_labor_1"]
        compare_data_frame["Всего машино часов"] = compare_data_frame["ОБЪЕМ 1 - У.4"] * compare_data_frame[
            "avg_mach_1"]
        # compare_data_frame = compare_data_frame[compare_data_frame["ОБЪЕМ 1 - У.4"] > 0]
        compare_data_frame.to_excel("Calculated total hours.xlsx", index=False)
        print("Computed total hours could be found in Calculated total hours Excel file.")
        return compare_data_frame

    @staticmethod
    def missing_norms(data: pd.DataFrame) -> pd.DataFrame:
        """Method that finds all missing norms if quantity1 is not equal to 0, labor and machine hours are equal to 0"""

        missing_norms = []
        iterable_data = data.itertuples(index=False, name=None)
        for code in iterable_data:
            if code[1] == 0 and code[2] == 0 and code[3] != 0:
                missing_norms.append(code)
        missing_norms_dataframe = pd.DataFrame(missing_norms)
        return missing_norms_dataframe

    def save_missing_norms_as_level4(self, missing_norms: pd.DataFrame) -> list[Level4]:
        """Method that stores previously contained DataFrame as objects of class Level4, for easier manipulation."""

        level4 = []

        try:
            data_code = self.connect_to_a_file_and_read_content_codes()

            data_merged = missing_norms.merge(data_code, left_on=0, right_on="Позиции дла Контрактации")
            iterable_data = data_merged.itertuples(index=False, name=None)
            for code in iterable_data:
                level4.append(Level4(name_level4=code[0], description_level4=code[7], unit_measure_l4_1=code[8],
                                     unit_measure_l4_2=code[9], unit_measure_l4_3=code[10], avg_labor_1=0, avg_mach_1=0))
            return level4
        except KeyError:
            print("There are no missing norms")
        except AttributeError:
            print("There are no missing norms")

    def add_norms_console(self, missing_norms: list[Level4]) -> list[Level4]:
        """Method that allows users to input average norms that are missing,
        and adds them to base class list for later use."""
        try:
            print(f"There are {len(missing_norms)} missing norms.")
            for code in missing_norms:
                print(f"Code: {code.name_level4} Measure: {code.unit_measure_l4_1}")
                code.avg_labor_1 = self.test_user_input_float_hours("labor")
                code.avg_mach_1 = self.test_user_input_float_hours("machine")
                self.list_of_norms.append(code)
            return self.list_of_norms
        except TypeError:
            print("No missing norms")

    def merge_results_level4(self, input0: pd.DataFrame, recalculated: pd.DataFrame,) -> pd.DataFrame:
        """Method that sums all calculated average totals and all hour totals based on norming process.
        This DataFrame is going to make it easier to compare results of hours gained by average norms with
        hours gained by the norming process."""

        rev1 = self.group_and_sum_data_level4(recalculated)
        rev0 = InputFile.group_and_sum_data_level4(input0)
        print(rev0)
        data_merged = rev1.merge(rev0, how="left", on="Уровень 4")
        return data_merged

    @staticmethod
    def show_difference(data_merged: pd.DataFrame) -> dict:
        """This method compares results of file with norms and without norms. It iterates through data gained by the
        merge_results_level4 method. It calculates percentage difference of quantity1(it should be almost the same but
        there are some exceptions), percentage difference of total labor and machine hours. It creates a file Analysis
        with all percentage differences and codes that are new in separate sheets."""

        data_iterable = data_merged.itertuples(index=False, name=None)
        dictionary = {"Code": [], "Percentage difference quantity": [], "Percentage difference labor hours": [],
                      "Percentage difference machine hours": []}
        missing_codes = {"Code": [], "Quantity": [], "Total labor hours": [], "Total machine hours": []}
        for code in data_iterable:
            if not math.isnan(code[6]):
                dictionary["Code"].append(code[0])
                difference = abs(code[3] - code[8])
                average = (code[3] + code[8]) / 2
                percent = round((difference / average) * 100, 0)
                dictionary["Percentage difference quantity"].append(percent)
                if code[6] != 0:
                    difference = abs(code[1] - code[6])
                    average = (code[1] + code[6]) / 2
                    percent = round((difference / average) * 100, 0)
                    dictionary["Percentage difference labor hours"].append(percent)
                else:
                    dictionary["Percentage difference labor hours"].append(0)
                if code[7] != 0:
                    difference = abs(code[2] - code[7])
                    average = (code[2] + code[7]) / 2
                    percent = round((difference / average) * 100, 2)
                    dictionary["Percentage difference machine hours"].append(percent)
                else:
                    dictionary["Percentage difference machine hours"].append(0)
            else:
                missing_codes["Code"].append(code[0])
                missing_codes["Quantity"].append(code[3])
                missing_codes["Total labor hours"].append(code[1])
                missing_codes["Total machine hours"].append(code[2])

        df = pd.DataFrame(dictionary)
        df_missing = pd.DataFrame(missing_codes)
        with pd.ExcelWriter("Analysis.xlsx") as writer:
            df.to_excel(writer, sheet_name="Percent_analysis", index=False)
            df_missing.to_excel(writer, sheet_name="New_codes", index=False)
        return dictionary

    def proceed_with_second_stage_of_the_program(self, base_data_no_norms):
        """Method that combines previous methods in order to create new Average norm file."""

        try:
            data_with_total_hours = self.calculate_total_avg_hours_rev1(base_data_no_norms)
            grouped_data = self.group_and_sum_data_level4(data_with_total_hours)
            missing_total_hours = self.missing_norms(grouped_data)
            missing = self.save_missing_norms_as_level4(missing_total_hours)
            self.add_norms_console(missing)
            self.create_a_file_with_average_norms()
        except FileNotFoundError:
            print("Due to failed average norm creation, file Average norm has not been created.")
        except PermissionError:
            print("File is open.")
        except TypeError:
            print("There is a string somewhere in the data and it is supposed to be a number.")

    def recalculate_total_hours(self, data: pd.DataFrame) -> pd.DataFrame:
        """Method that computes total hours based on the Average norm file, and returns grouped values by codes."""
        try:
            print("Recalculating total hours...")
            recalculated = self.calculate_total_avg_hours_rev1(data)
            return self.group_and_sum_data_level4(recalculated)
        except FileNotFoundError:
            print("Due to failed average norm creation, file Average norm has not been created.")
        except PermissionError:
            print("File is open.")
        except TypeError:
            print("There is a string somewhere in the data and it is supposed to be a number.")

    def compare_results(self, data_rev0, data_rev0_average_total) -> dict:
        """Method that returns merged results of two separate files and stores disputed codes if there are any.
        Those code would contain percentage difference in hours greater then 15%"""
        try:
            merged_results = self.merge_results_level4(data_rev0, data_rev0_average_total)
            return self.show_difference(merged_results)
        except AttributeError:
            print("Can't generate report, missing data.")

    @staticmethod
    def check_if_there_are_any_codes_with_difference_grater_than_15percent(dictionary: dict) -> list:
        """If percentage difference of hours is greater than percentage difference of quantity1 + allowed 15 percent
        variation those codes are then stored in a list. If the user wants to manually change average norms, and then
        recompute total hours."""
        try:
            counter = len(dictionary["Code"])
            check_average = []
            for code in range(counter - 1):
                limit_up = dictionary["Percentage difference quantity"][code] + 15
                limit_down = dictionary["Percentage difference quantity"][code] - 15
                labor_percentage = dictionary["Percentage difference labor hours"][code]
                machine_percentage = dictionary["Percentage difference machine hours"][code]
                if labor_percentage > limit_up or machine_percentage > limit_up or labor_percentage < limit_down \
                        or machine_percentage < limit_down:
                    check_average.append(dictionary["Code"][code])
            return check_average
        except TypeError:
            print("Counter value is none because there is no dictionary.")

    def adopt_norms_if_there_are_no_disputed_codes(self, data_rev1: pd.DataFrame) -> pd.DataFrame:
        """If there are no questionable codes and norms, this function adopts previously calculated average norms and
        recomputes new file with changed quantities."""

        self.proceed_with_second_stage_of_the_program(data_rev1)
        data_adopted = self.recalculate_total_hours(data_rev1)
        print("Process is finished. You can find computed file in Calculated total hours.")
        return data_adopted

    @staticmethod
    def show_options_if_norms_are_adopted() -> int:
        """Method that shows user options if norms are adopted."""

        print("Write 0, to visualise data based on level 0.")
        print("Write 1, to visualise data based on level 1.")
        print("Write 2, to visualise data based on level 2.")
        print("Write 3, to visualise data based on level 3.")
        print("Write 4, to visualise data based on level 4.")
        print("Write 5, to exit the program.")
        while True:
            try:
                user_input = int(input("Input value from 0 to 5 to choose next action: "))
                if user_input in range(0, 6):
                    return user_input
                else:
                    print("Wrong parameter, try again.")
            except ValueError:
                print("Wrong parameter, try again.")
    @staticmethod
    def group_data_for_visualisation_levl0(data: pd.DataFrame):
        column = "Уровень 0"
        grouped = FileWithoutNorms.group_and_sum_data_level0(data)
        show_lab_hours(grouped, column)
        show_mach_hours(grouped, column)

    @staticmethod
    def group_data_for_visualisation_levl1(data: pd.DataFrame):
        column = "Уровень 1"
        grouped = FileWithoutNorms.group_and_sum_data_level1(data)
        show_lab_hours(grouped, column)
        show_mach_hours(grouped, column)

    @staticmethod
    def group_data_for_visualisation_levl2(data: pd.DataFrame):
        column = "Уровень 2"
        grouped = FileWithoutNorms.group_and_sum_data_level2(data)
        show_lab_hours(grouped, column)
        show_mach_hours(grouped, column)

    @staticmethod
    def group_data_for_visualisation_levl3(data: pd.DataFrame):
        column = "Уровень 3"
        grouped = FileWithoutNorms.group_and_sum_data_level3(data)
        show_lab_hours(grouped, column)
        show_mach_hours(grouped, column)

    @staticmethod
    def group_data_for_visualisation_levl4(data: pd.DataFrame):
        column = "Уровень 4"
        grouped = FileWithoutNorms.group_and_sum_data_level4(data)
        show_lab_hours(grouped, column)
        show_mach_hours(grouped, column)

    @staticmethod
    def allow_user_to_choose_or_exit():
        """Method that visualises data based on user input or ends the program."""

        try:
            data = pd.read_excel("Calculated total hours.xlsx")
            latest_data = pd.DataFrame(data)
            while True:
                input_user = FileWithoutNorms.show_options_if_norms_are_adopted()
                if input_user == 0:
                    FileWithoutNorms.group_data_for_visualisation_levl0(latest_data)
                elif input_user == 1:
                    FileWithoutNorms.group_data_for_visualisation_levl1(latest_data)
                elif input_user == 2:
                    FileWithoutNorms.group_data_for_visualisation_levl2(latest_data)
                elif input_user == 3:
                    FileWithoutNorms.group_data_for_visualisation_levl3(latest_data)
                elif input_user == 4:
                    FileWithoutNorms.group_data_for_visualisation_levl4(latest_data)
                elif input_user == 5:
                    print("The program is closed.")
                    break
                else:
                    print("Wrong parameters.")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(e.__str__())

    @staticmethod
    def save_additional_report_group_data_objects() -> pd.DataFrame:
        """Method that saves additional Excel file that shows quantities and total hours distribution
        base on codes and objects."""
        try:
            data = pd.read_excel("Calculated total hours.xlsx")
            latest_data = pd.DataFrame(data)

            report = latest_data.groupby(["Уровень 4", "Шифр подобъекта"])[["Всего человеко часов",
                                                                            "Всего машино часов",
                                                                            "ОБЪЕМ 1 - У.4", "ОБЪЕМ 2 - У.4",
                                                                            "ОБЪЕМ 3 - У.4"]].sum()
            report.to_excel("Additional.xlsx")
            return report
        except FileNotFoundError:
            print("Missing file.")
        except Exception as e:
            print(e.__str__())









