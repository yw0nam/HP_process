# python data_grouping.py --folder data_with_family_hx --dataset_name any_bx
python define_covarites.py --folder data_with_family_hx --dataset_name bx_for_hp
python merge_cancer_fill_na.py --folder data_with_family_hx --dataset_name bx_for_hp
python merge_updated_death.py --folder data_with_family_hx --dataset_name bx_for_hp
python merge_final_fu_date.py --folder data_with_family_hx --dataset_name bx_for_hp
python valid_data_len_fu.py --folder data_with_family_hx --dataset_name bx_for_hp