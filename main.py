
from working_with_files.abstract_file_class import InputFile, check_if_file_exists
from working_with_files.file_with_norms_class import FileWithNorms
from working_with_files.file_withouth_norms import FileWithoutNorms


if __name__ == "__main__":

    """First stage of the program is to create average norms based on the input file that contains total hours.
    The input file is called "test rev0 with norms.xlsx" (), and it is a standard output for norming department after 
    finishing the norming process, position by position. In this first stage, user is required to input valid path and 
    name of the input file, and later if needed fill missing norms through console. Missing norms are only going to show
    up if there has been a mistake in the norming process, and quantity1 has been set to 0. Output of this stage is 
    an Excel file containing computed or/and manually added average norms"""

    file_path, file_name = check_if_file_exists()  # Make sure the user input is correct before initializing object
    file_with_norms_rev0 = FileWithNorms(file_path=file_path, file_name=file_name)
    data_rev0_with_norms = file_with_norms_rev0.connect_to_a_file_and_read_content()
    average_norms_base_data = file_with_norms_rev0.start_the_program_and_create_avg_norms(base_data=data_rev0_with_norms)

    """Second stage of the process is to find new codes and missing norms.
    To validate previously calculated average norms, we input output product
    file of department creating Bill of Quantities. Both files are based on the same positions and quantities (minor
    differences if norming departament changes some Level 4 codes) so the total labor and machine hours calculated
    with average norms should not vary too much from the output product of the norming department.
    The user is going to be required to input name and path of the standard output file of the department creating 
    Bill of Quantities (in this case "test rev0 no norms.xlsx"). The user is going to be required to input missing
    average norms if needed."""

    file_path, file_name = check_if_file_exists() # Make sure the user input is correct before initializing object
    file_without_norms_rev0 = FileWithoutNorms(file_path=file_path, file_name=file_name)
    data_rev0_without_norms = file_without_norms_rev0.connect_to_a_file_and_read_content()
    file_without_norms_rev0.proceed_with_second_stage_of_the_program(base_data_no_norms=data_rev0_without_norms)

    """Now that all norms are established we move on to a next stage.
    Third stage of the program is to compute total hours based on the average norms"""

    data_REV0_with_total_average_norms = file_without_norms_rev0.recalculate_total_hours(data=data_rev0_without_norms)

    """It is necessary to compare actual total hours (output file of norming department) and average total hours based 
    on the same quantities (output file Bill of Quantities multiplied with average norms) in case 
    average norms need changes and percent differences in total hours are greater then 15 percent. This stage allows the
    user to validate average norms and later adopt them for actual new revision, or change of quantities."""
    grouped_rev0_with_norms = file_with_norms_rev0.group_and_sum_data_level4(data_rev0_with_norms)
    analysis = file_without_norms_rev0.compare_results(data_rev0=grouped_rev0_with_norms,
                                                       data_rev0_average_total=data_REV0_with_total_average_norms)
    disputed_code = file_without_norms_rev0.check_if_there_are_any_codes_with_difference_grater_than_15percent(analysis)

    """After comparing total hours gained by the norming process with total hours gained with average hours,
    if there is no percentage difference greater then 15, we can input new file with changed quantities
    (actual revision "test rev1.xlsx") and finish the process of analysis."""
    try:
        if len(disputed_code) == 0:
            file_path, file_name = check_if_file_exists()  # Make sure user input is correct before initializing object
            file_rev1 = FileWithoutNorms(file_path, file_name)
            data_file_rev1 = file_rev1.connect_to_a_file_and_read_content()
            file_rev1.adopt_norms_if_there_are_no_disputed_codes(data_rev1=data_file_rev1)
            FileWithoutNorms.save_additional_report_group_data_objects()
            FileWithoutNorms.allow_user_to_choose_or_exit()
        else:
            print(f"Codes that should be revised: {disputed_code}\nThere has been a mistake in the norming process"
                  f"whilst defining leading positions and quantities.")
    except TypeError:
        print("Type None is not a list. Failed to create a list.")

    """Final result of the program is Excel file "Average norms.xlsx" containing calculated average norms., file 
    "Calculated total hours.xlsx" that contains all positions from the Bill of Quantities but with computed total hours.
    "Analysis.xlsx" file that contains percentage differences and new codes. "Additional.xlsx" file that contains 
     grouped data based on the codes and objects"""




