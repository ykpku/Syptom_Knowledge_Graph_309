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

syptom_save_list = set([])
labtest_save_list = set([])
phy_save_list = set([])
phy_condition_save_list = set([])

for icol in range(1, len(xlsx_data)):
	disease_hist_temp = []
	phy_indic_temp = []
	labtest_temp = []
	syptom_list_temp = []
	disease_list.append(str.strip(xlsx_data[icol][1]))
	for irow in range(2, len(xlsx_data[0])):
		if xlsx_data[icol][irow] is not None:
			dt = nu_dis.key_word_extract(xlsx_data[icol][irow], [i[0] for i in disease_data])
			disease_hist_temp.extend(dt)
			if len(dt) == 0:
				phy_t = nu_lab.get_suv_from_text(xlsx_data[icol][irow])
				if len(phy_t) > 0:
					phy_indic_temp.append(phy_t)
					########## save #############
					for phy_t_i in phy_t:
						phy_sp = phy_t_i.split("##")
						phy_save_list.add(phy_sp[0])
						phy_condition_save_list.add(phy_sp[1])
					#############################
					if xlsx_data[icol][irow].find("：") != -1:
						i_end = xlsx_data[icol][irow].find("：")
						labtest_temp.append(xlsx_data[icol][irow][3:i_end])
					else:
						labtest_temp.append("望闻问切")
					########## save #############
					labtest_save_list.add(labtest_temp[-1])
					#############################
				else:
					st = nu_syp.key_word_extract(xlsx_data[icol][irow], [i[0] for i in syptom_data])
					syptom_list_temp.extend(st)
					for st_i in st:
						syptom_save_list.add(st_i)
	disease_hist.append(disease_hist_temp)
	phy_indic.append(phy_indic_temp)
	labtest_list.append(labtest_temp)
	syptom_list.append(syptom_list_temp)

phy_condition_relation_save = []
for item in range(len(disease_list)):
	print(disease_list[item], "---", disease_hist[item], "---", labtest_list[item], "---", phy_indic[item], "---", syptom_list[item])
	phy_condition_relation_save.append([y for x in phy_indic[item] for y in x])


CsvUtility.write_word_dict("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\疾病实例.csv", disease_list)
CsvUtility.write_word_dict("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\症状实例.csv", syptom_save_list)
CsvUtility.write_word_dict("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\生理指标实例.csv", phy_save_list)
CsvUtility.write_word_dict("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\检验检查实例.csv", labtest_save_list)
CsvUtility.write_word_dict("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\指标条件实例.csv", set([y for x in phy_condition_relation_save for y in x]))

CsvUtility.write_relation("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\病史关系.csv", disease_list, disease_hist)
CsvUtility.write_relation("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\疾病-指标条件关系.csv", disease_list, phy_condition_relation_save)
CsvUtility.write_relation("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\指标条件-指标关系.csv", [y for x in phy_condition_relation_save for y in x], [[y.split("##")[0]] for x in phy_condition_relation_save for y in x])
CsvUtility.write_relation("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\疾病症状关系.csv", disease_list, syptom_list)
CsvUtility.write_relation("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\生理指标-检验检查关系.csv", [y for x in labtest_list for y in x], [y for x in phy_indic for y in x])

