from Utils.xlsx_utility import XlsxUtility
from Utils.nlp_utility import NLPUtility
from Utils.csv_utility import CsvUtility

xlsx_data = XlsxUtility.get_sheet_data("D:\\桌面\\医疗项目\\309医院EHR数据", "病历诊断等 - 20190604.xlsx", 2, True)

disease_data = CsvUtility.reform_word_dict("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\疾病字典.csv")
CsvUtility.write_word_dict("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\疾病字典_ltp.csv", [i[0] for i in disease_data])
nu_dis = NLPUtility(word_pattern_file="D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\疾病字典_ltp.csv")
nu_dis.load_jieba_model()

nu_lab = NLPUtility()
nu_lab.load_ltp_model()

syptom_data = CsvUtility.reform_word_dict("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\症状字典.csv")
CsvUtility.write_word_dict("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\症状字典_ltp.csv", [i[0] for i in syptom_data])
nu_syp = NLPUtility(word_pattern_file="D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\症状字典_ltp.csv")
nu_syp.load_jieba_model()

disease_list = []
disease_hist = []
phy_indic = []
labtest_list = []
syptom_list = []

for icol in range(1, len(xlsx_data)):
	disease_hist_temp = []
	phy_indic_temp = []
	labtest_temp = []
	syptom_list_temp  =[]
	disease_list.append(str.strip(xlsx_data[icol][1]))
	for irow in range(2, len(xlsx_data[0])):
		if xlsx_data[icol][irow] is not None:
			dt = nu_dis.key_word_extract(xlsx_data[icol][irow], [i[0] for i in disease_data])
			disease_hist_temp.extend(dt)
			if len(dt) == 0:
				phy_t = nu_lab.get_suv_from_text(xlsx_data[icol][irow])
				if len(phy_t) > 0:
					phy_indic_temp.append(phy_t)
					if xlsx_data[icol][irow].find("：") != -1:
						i_end = xlsx_data[icol][irow].find("：")
						labtest_temp.append(xlsx_data[icol][irow][3:i_end])
					else:
						labtest_temp.append("望闻问切")
				else:
					st = nu_syp.key_word_extract(xlsx_data[icol][irow], [i[0] for i in syptom_data])
					syptom_list_temp.extend(st)
	disease_hist.append(disease_hist_temp)
	phy_indic.append(phy_indic_temp)
	labtest_list.append(labtest_temp)
	syptom_list.append(syptom_list_temp)


for item in range(len(disease_list)):
	print(disease_list[item],"---", disease_hist[item],"---", labtest_list[item],"---", phy_indic[item],"---", syptom_list[item])
