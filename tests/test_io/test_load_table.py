import laser_beam as lb
# C:\Users\robert.boge\OneDrive - ELI Beamlines\Dokumenty\07 Software\Python\2026_Laser_Beam\laser_beam\tests\test_io\Example.xlsx
folder = r'tests\test_io'
#raw = lb.load_table_as_dataset(folder = folder, file_name="Example.xlsx")

data_dict = lb.load_table_to_flat_dict(folder = folder, file_name="Example.xlsx")

data_dict['new_key'] = 'new_value'

ds = lb.flat_dict_to_dataset(data_dict)


# dict = ds.to_dict()

data_dict_2 = lb.dataset_to_flat_dict(ds)

lb.flat_dict_to_excel(
    flat_dict=data_dict_2,
    file_name= r'tests\test_io\Example_2.xlsx', 
)

# print(f"data_dict: {data_dict}")
# print(f"ds: {ds}")
# print(f"dict: {dict}")

print("end")