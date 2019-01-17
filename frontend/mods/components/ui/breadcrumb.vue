<template>
	<div class="c-breadcrumb">
		<div class="breadcrumb">
			<span class="location-hint">
				<i class="el-icon-location"></i>
				页面当前位置：
			</span>
			<el-breadcrumb separator-class="el-icon-arrow-right">
				<el-breadcrumb-item :to="{ path: '/' }">
					首页
				</el-breadcrumb-item>
				<el-breadcrumb-item v-for="item in bread" :key="item.path" :to="{ path: '/' + item.path }">
					{{ item.title }}
				</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<el-collapse class="work-process">
			<el-collapse-item>
				<template slot="title">
					<i class="iconfont icon-gongzuoliucheng"></i>查看工作流程
    			</template>
				<div v-for="(item, index) in processDict[curPath]" :key="index">
					{{ item }}
				</div>
			</el-collapse-item>
		</el-collapse>	
	</div>
</template>

<script>
export default {
	name: 'breadcrumb',
	data() {
		return {
			breadDict: {
				'train': '检测模型训练子平台',
				'upload': '数据获取',
				'feature': '特征提取',
				'cluster': '聚类标记',
				'semiSupervised': '半监督学习',
				'check': '恶意检测',
				'identify': '恶意访问识别子平台',
				'label': '辅助人工标记工具'
			},
			bread: [{
				path: 'train',
				title: "检测模型训练子平台"
			}, {
				path: 'upload',
				title: "数据获取"
			}],
			curPath: 'upload',
			processDict: {
				'upload': ['1.上传自行生成的RSA公钥，用于系统对用户标识加密;',
					'2.上传用户的URL访问日志，用于模型训练。'],
				'check': ['1. 上传待检测的用户URL访问日志;',
					'2. 选择要使用的检测模型，确认模型相关参数并<开始检测>按钮进行识别;',
					'3. 查看结果类别，若检测错误进入辅助人工标记页面修改类别。'],
				'feature': ['1.选择合适的特征提取参数然后开始量化特征吧！以下为可配置参数的说明：',
					'a） 访问正常时间：您认为该园区内较正常的上网时间范围，用于计算特征<异常时间频发度>',
					'b） 时间窗口：特征<时间窗口域名访问相似度>的时间窗口大小',
					'c） 设备类型参数：URL参数中常用作设备类型的关键字，用于补充特征<设备类型异样性>的设备类型字典'],
				'cluster': ['1.点击<开始聚类>按钮进行样本的聚类标记；',
					'a）按钮状态说明：<聚类中>表示聚类算法正在运行，<上次聚类完成，重新聚类>表示上次聚类标记已完成，若有其他更改可重新开始。',
					'2.聚类完成后，点击<下一步>并可根据下方的聚类结果选择操作：',
					'a）若对结果不满意或需要确认类别标记，可点击<人工辅助标记>按钮；',
					'b）若满意，可点击<下一模块>按钮，进入半监督学习流程。'],
				'label': [
					'1. 观察该条样本的访问次数折线图和访问参数列表;',
					'2. 若本页存在标记不正确样本，修改开关状态后点击<保存并下一页>完成校正。',
					'注）善意标记为“关”，恶意标记为“开”。'],
				'semiSupervised': [
					'1.填写合适的模型参数候选列表或者选用系统默认参数;',
					'a） 选用数据集大小：用于参与训练的数据集数量，包含训练集与测试集，默认二者比例为9：1',
					'b） 标注样本比例：用于S4VM算法学习的已标注样本占选用数据集比例',
					'c） 交叉验证折数：用于提高模型的泛化能力，确定模型参数的数据切分份数',
					'd） S4VM算法参数候选值：包含S4VM算法的惩罚参数C1,C2和RBF核函数的gamma',
					'2.点击<开始训练>进行半监督学习。',
					'a） 模块进入学习过程中时，按钮将变为<进行中>；当训练完成后，按钮变为<训练已完成>状态',
				],
			}

		}
	},
	watch: {
		$route(to, from) {
			let paths = to.path.split('/');
			paths.shift();
			let newBread = []
			paths.forEach(path => {
				newBread.push({
					path,
					title: this.breadDict[path]
				});
				this.curPath = path;
			});
			this.bread = newBread;
		}
	},
}
</script>

<style lang="less">
.c-breadcrumb {
	i {
		color: #409eff;
	}
	.breadcrumb {
		display: flex;
		align-items: center;
		.location-hint {
			font-weight: 800;
			font-size: 14px;
		}
	}
	.work-process {
		margin: 15px 0;
		.icon-gongzuoliucheng {
			margin-right: 2px;
		}
		.el-collapse-item__wrap, .el-collapse-item__header {
			background: #efefef;
		}
		.el-collapse-item__header {
			font-size: 14px;
			color: #000;
			font-weight: 800;
		}
		.el-collapse-item__content > div {
			margin-left: 30px;
		}
	}
}
</style>
