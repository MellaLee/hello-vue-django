# 由于原数据中黑样本过少，需要伪造黑样本使得黑白样本的比例为1：1
# just for importing models of django
import os
import sys
import django
import random
sys.path.append("../..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from backendModels.models import User, QuantitativeLog

# 默认伪造数据的user_id=1
originDataId = 977213
fakeDataId = 1954399
def fakeEuc(value):
	if (value <= 100):
		return value + random.uniform(-3, 3)
	else:
		return value + random.uniform(-10, 10)

def fakePro(value):
	if (value < 2):
		return random.uniform(0, 2)
	else:
		return value + random.uniform(-2, 2)

def fake():
	log = QuantitativeLog.objects.filter(label=1)
	# 计算每一个黑样本需要伪造的样本数量
	eachLabel1ToFakeNum = int((originDataId - len(log)) / len(log))
	for index, model in enumerate(log):
		quantitativeLogList = []
		for i in range(0, eachLabel1ToFakeNum):
			quantitativeLogList.append(QuantitativeLog(
				url='fake' + str(index * eachLabel1ToFakeNum + i),
				user_id = 1,
				similarEuc=round(fakeEuc(model.similarEuc), 4),
				urlArgsEntropy=round(model.urlArgsEntropy + random.uniform(-0.5, 0.5), 4),
				abnormalTimeProbability=round(fakePro(model.abnormalTimeProbability), 4),
				sameArgsDiversity=round(random.uniform(0.63, 0.86), 4),
				webClassify=round(random.uniform(0.82, 1), 4),
				predict_label=0,
				label=1,
				cluster_label=0
			))

		print (len(quantitativeLogList))
		for i in range(0, len(quantitativeLogList), 200):
			QuantitativeLog.objects.bulk_create(quantitativeLogList[i:i + 200])

def startRun():
	fake()