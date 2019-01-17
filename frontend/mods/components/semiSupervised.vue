<template>
	<div class="c-semi">
		<div class="semi">
			<i class="iconfont icon-tiao"></i>模型训练
			<el-form class="semi-form" :inline="true" :model="form">
				<el-form-item label="选用数据集大小">
					<el-input v-model="form.amount" :placeholder='"当前可用样本共" + sampleAmount + "个"'></el-input>
				</el-form-item>
				<el-form-item label="标注样本比例">
					<el-input v-model="form.ratio" placeholder="标注样本占选用数据集比例"></el-input>
				</el-form-item>
				<el-form-item label="交叉验证折数">
					<el-input v-model="form.cv" placeholder="交叉验证折数"></el-input>
				</el-form-item>
			</el-form>
			<el-form class="semi-form2" :inline="true" :model="form">
				<el-form-item label="S4VM算法参数候选值">
					<span class="hint">*以半角逗号分隔参数列表</span>
					<el-input v-model="form.c1" placeholder="惩罚参数C1形如0.4,4,40"></el-input>
				</el-form-item>
				<el-form-item>
					<el-input v-model="form.c2" placeholder="惩罚参数C2"></el-input>
				</el-form-item>
				<el-form-item>
					<el-input v-model="form.gamma" placeholder="RBF核函数系数gamma"></el-input>
				</el-form-item>
				<el-form-item style="float:right">
					<el-button type="success" @click="selectSysArgs" plain>选用系统参数</el-button>
					<el-button type="primary" @click="onSubmit" plain>开始训练</el-button>
				</el-form-item>
			</el-form>
		</div>
		<div class="result">
			<i class="iconfont icon-tiao">训练结果列表（误报率为1%）</i>
			<el-table :data="tableData">
				<el-table-column type="index"></el-table-column>
				<el-table-column label="模型参数">
					<template slot-scope="scope">
						<span v-for="(item,key) in scope.row.args.split(',')" :key="key">
							{{ item }}<br>
						</span>
					</template>
				</el-table-column>
				<el-table-column width="650" label="ROC曲线">
					<template slot-scope="scope">
						<img :src="scope.row.img">
					</template>
				</el-table-column>
				<el-table-column prop="auc" label="AUC值"></el-table-column>
				<el-table-column prop="rate" label="检出率"></el-table-column>
				<el-table-column prop="time" label="运行时间（min）"></el-table-column>
				<el-table-column label="操作" align="center">
					<template slot-scope="scope">
						<el-button type="primary" @click="onSubmit" plain>保存模型</el-button>
					</template>
				</el-table-column>
			</el-table>
			<el-pagination class="page"
				background
				layout="prev, pager, next"
				:total="11">
			</el-pagination>
		</div>
		`
	</div>
</template>

<script>
export default {
	name: 'semi',
	data() {
		return {
			sampleAmount: 20000,
			form: {
				amount: '',
				ratio: '',
				cv: '',
				c1: '',
				c2: '',
				gamma: ''
			},
			tableData: [{
				args: 'C1:40,C2:10,gamma:0.2',
				img: 'static/image/semi/1.png',
				auc: '0.95',
				rate: '88.7%',
				time: '23.5'
			}]
		};
	},
	created() {
		this.$store.dispatch('setStepNum', 0);
	},
	methods: {
		onSubmit() {
			// TODO 
		},
		selectSysArgs() {
			this.form.amount = this.sampleAmount;
			this.form.ratio = '33.3%';
			this.form.cv = 10;
			this.form.c1 = 40;
			this.form.c2 = 10;
			this.form.gamma = 0.2;
		}
	} 

}
</script>

<style lang="less">
.c-semi {
	.semi-form {
		margin-left: 13px;
		margin-top: 5px;
	}
	.semi-form2 {
		margin-left: 13px;
		.hint {
			position: absolute;
			left: -145px;
			top: 30px;
			font-size: 12px;
			color: #f56c6c;
		}
	}
	.result {
		margin-top: 15px;
		img {
			height: 350px;
		}
	}
	.page {
		float: right;
	}
}
</style>
