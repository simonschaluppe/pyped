
import xlwings as xw



def sanitize(filepath="../../data/PEQ_CHEQ.xlsm"):
    """takes an excel of any type and generates a standardized 'clean_PED_...xlsx' """

    #
    source_book = xw.Book(filepath, read_only=False)

    # create new book
    template_path = "../../data/clean/Clean_template.xlsx"
    standard_book = xw.Book(template_path, read_only=False)

    sb = standard_book
    #transform
    #if source type = PEQ CHEQ
    calc_data = source_book\
        .sheets["Calculation"]\
        .tables["calc_variables"]\
        .data_body_range\
        .value


    print(calc_data)

    meta = standard_book.sheets["meta"].tables["meta"].data_body_range.value

    meta[0][1] = source_book.fullname
    from datetime import datetime
    meta[1][1] = str(datetime.now())[:19]

    standard_book.sheets["meta"].tables["meta"].data_body_range.value = meta


    #save book
    save_path = "../../data/clean/Clean_testped3.xlsx"
    sb.save(save_path)


if __name__ == "__main__":

    import os
    print(os.getcwd())
    sanitize()
