from Utils.xlsx_utility import XlsxUtility
from Utils.nlp_utility import NLPUtility


xlsx_data = XlsxUtility.get_sheet_data("D:\\桌面\\医疗项目\\309医院EHR数据", "病历诊断等 - 20190604.xlsx", 2, True)
disease_list = []
phy_indic = []
labtest_list = []
nu = NLPUtility()
nu.load_ltp_model()
for icol in range(1, len(xlsx_data)):
	phy_indic_temp = []
	labtest_temp = []
	disease_list.append(str.strip(xlsx_data[icol][1]))
	for irow in range(2, len(xlsx_data[0])):
		if xlsx_data[icol][irow] != None:
			phy_t = nu.get_suv_from_text(xlsx_data[icol][irow])
			if len(phy_t) > 0:
				phy_indic_temp.append(phy_t)
				if xlsx_data[icol][irow].find("：") != -1:
					i_end = xlsx_data[icol][irow].find("：")
					labtest_temp.append(xlsx_data[icol][irow][3:i_end])
				else:
					labtest_temp.append("望闻问切")

	phy_indic.append(phy_indic_temp)
	labtest_list.append(labtest_temp)
print(disease_list)
print(phy_indic)
print(labtest_list)



