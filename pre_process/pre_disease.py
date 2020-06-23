from Utils.xlsx_utility import XlsxUtility
from Utils.nlp_utility import NLPUtility
from Utils.csv_utility import CsvUtility

xlsx_data = XlsxUtility.get_sheet_data("D:\\桌面\\医疗项目\\309医院EHR数据", "病历诊断等 - 20190604.xlsx", 2, True)
disease_data = CsvUtility.reform_word_dict("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\疾病字典.csv")
CsvUtility.write_word_dict("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\疾病字典_ltp.csv", [i[0] for i in disease_data])
nu = NLPUtility(word_pattern_file="D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\疾病字典_ltp.csv")
nu.load_jieba_model()
# print(disease_data)
disease_list = []
disease_hist = []
for icol in range(1, len(xlsx_data)):
	disease_hist_temp = []
	disease_list.append(str.strip(xlsx_data[icol][1]))
	for irow in range(2, len(xlsx_data[0])):
		if xlsx_data[icol][irow] != None:
			disease_hist_temp.extend(nu.key_word_extract(xlsx_data[icol][irow], [i[0] for i in disease_data]))
	disease_hist.append(disease_hist_temp)
print(disease_list)
print(disease_hist)