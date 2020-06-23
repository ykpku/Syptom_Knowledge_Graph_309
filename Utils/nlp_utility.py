# Set your own model path
MODELDIR = "H:\\new_github_workspace\\Syptom_Knowledge_Graph_309\\ltp_data_v3.4.0"

import sys
import os
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SentenceSplitter
import jieba
from Utils.csv_utility import CsvUtility

class NLPUtility(object):
	def __init__(self, word_pattern_file="H:\\new_github_workspace\\Syptom_Knowledge_Graph_309\\test_result.csv"):

		self.word_pattern_file = word_pattern_file
		self.segmentor = Segmentor()
		self.postagger = Postagger()
		self.parser = Parser()
		self.recognizer = NamedEntityRecognizer()

	def load_ltp_model(self):
		print("正在加载LTP模型... ...")

		self.segmentor.load_with_lexicon(os.path.join(MODELDIR, "cws.model"), self.word_pattern_file)
		self.postagger.load(os.path.join(MODELDIR, "pos.model"))
		self.parser.load(os.path.join(MODELDIR, "parser.model"))
		self.recognizer.load(os.path.join(MODELDIR, "ner.model"))

		print("加载模型完毕。")

	def load_jieba_model(self):
		print("正在加载jieba模型... ...")
		jieba.load_userdict(self.word_pattern_file)
		print("加载模型完毕。")

	def key_word_extract(self, sentence, k_words):
		key_list = set([])
		seg_list = jieba.cut(sentence)
		# print(seg_list)
		for word in seg_list:
			if word in k_words:
				key_list.add(word)
		return list(key_list)


	def fact_triple_extract(self, sentence, segmentor, postagger, recognizer, parser, k_words):
		"""
		对于给定的句子进行事实三元组抽取
		Args:
			sentence: 要处理的语句
		"""
		# print sentence
		words = segmentor.segment(sentence)
		# print(list(words))
		# print "\t".join(words)
		postags = postagger.postag(words)
		# print(list(postags))
		netags = recognizer.recognize(words, postags)
		# print(list(netags))
		arcs = parser.parse(words, postags)
		# print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

		child_dict_list = self.build_parse_child_dict(words, arcs)
		result = []
		for index in range(len(postags)):
			# 抽取以谓词为中心的事实三元组
			if postags[index] == 'v' and words[index] in k_words:
				child_dict = child_dict_list[index]

				# 主谓
				if 'SBV' in child_dict.keys():
					for sub in child_dict['SBV']:
						e1 = self.complete_e(words, postags, child_dict_list, sub)
						r = words[index]
						# print("主语谓语关系\t(%s, %s)\n" % (e1, r))
						result.append(e1 + "##" + r)

						coo_child_dict = child_dict_list[sub]
						if 'COO' in coo_child_dict.keys():
							for i in range(len(coo_child_dict['COO'])):
								e2 = self.complete_e(words, postags, child_dict_list, coo_child_dict['COO'][i])
								# print("主语谓语关系\t(%s, %s)\n" % (e2, r))
								result.append(e2 + "##" + r)
		return result

	def build_parse_child_dict(self, words, arcs):
		"""
		为句子中的每个词语维护一个保存句法依存儿子节点的字典
		Args:
			words: 分词列表
			arcs: 句法依存列表
		"""
		child_dict_list = []
		for index in range(len(words)):
			child_dict = dict()
			for arc_index in range(len(arcs)):
				if arcs[arc_index].head == index + 1:
					if arcs[arc_index].relation in child_dict.keys():
						child_dict[arcs[arc_index].relation].append(arc_index)
					else:
						child_dict[arcs[arc_index].relation] = []
						child_dict[arcs[arc_index].relation].append(arc_index)
			# if child_dict.has_key('SBV'):
			#    print words[index],child_dict['SBV']
			child_dict_list.append(child_dict)
		return child_dict_list

	def complete_e(self, words, postags, child_dict_list, word_index):
		"""
		完善识别的部分实体
		"""
		child_dict = child_dict_list[word_index]
		prefix = ''
		if 'ATT' in child_dict.keys():
			for i in range(len(child_dict['ATT'])):
				prefix += self.complete_e(words, postags, child_dict_list, child_dict['ATT'][i])

		return prefix + words[word_index]

	def get_suv_from_text(self, text):
		k_words = CsvUtility.read_norm_array_csv(self.word_pattern_file)
		sents = SentenceSplitter.split(text)
		suv_list = []
		for sent in sents:
			suv_list.extend(self.fact_triple_extract(sent, self.segmentor, self.postagger, self.recognizer, self.parser, k_words))
		return suv_list

# nu = NLPUtility(word_pattern_file="D:/桌面/医疗项目/309医院EHR数据/数据处理\\ltp_dict.csv")
# kw = CsvUtility.read_norm_array_csv("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\ltp_dict.csv")
# print(kw)
# print(nu.key_word_extract(" （1）具有慢性支气管炎、肺气肿、急性上呼吸道感染, 流行性感冒, 慢性支气管炎, 慢性阻塞性肺疾病, 急性心肌梗死, 急性呼吸窘迫综合征, 急性心力衰竭, 低血糖症, 流行性脑脊髓膜炎等慢性肺疾病史。",k_words=CsvUtility.read_norm_array_csv("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\疾病字典_ltp.csv")))
# print(nu.key_word_extract(" 欧几里得是西元前三世纪的希腊数学家。",k_words=CsvUtility.read_norm_array_csv("D:\\桌面\\医疗项目\\309医院EHR数据\\数据处理\\ltp_dict.csv")))

# segmentor = Segmentor()  # 初始化实例
# CsvUtility.write_word_dict('D:/桌面/医疗项目/309医院EHR数据/数据处理/ltp_dict.txt', ['欧几里得'])
# segmentor.load_with_lexicon(os.path.join(MODELDIR, "cws.model"), 'D:/桌面/医疗项目/309医院EHR数据/数据处理/ltp_dict.txt') # 加载模型，参数lexicon是自定义词典的文件路径
# words = segmentor.segment('古代欧几里得和亚里士多德是西元前三世纪的希腊数学家。')
# print(' '.join(words))
# segmentor.release()

# import jieba
# CsvUtility.write_word_dict('D:/桌面/医疗项目/309医院EHR数据/数据处理/ltp_dict.txt', ['希腊数学家'])
# jieba.load_userdict("D:/桌面/医疗项目/309医院EHR数据/数据处理/ltp_dict.txt")
# seg_list = jieba.cut("古代欧几里得和亚里士多德是西元前三世纪的希腊数学家。")  # 默认是精确模式
# print(", ".join(seg_list))
