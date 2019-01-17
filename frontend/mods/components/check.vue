<template>
	<div class="c-check">
		<el-row :gutter="10">
			<el-col :span="12">
				<i class="iconfont icon-tiao"></i>检测URL访问日志
			</el-col>
		</el-row>
		<el-row :class="'upload-content active-' + activeItem" :gutter="10">
			<el-steps class="upload-step" direction="vertical" :active="activeItem">
				<el-step title="步骤1：上传待检日志"
					description="你想要检测的访问记录"
					icon="el-icon-document"
				></el-step>
				<el-step title="步骤2：选择要使用的检测模型"
					icon="iconfont icon-jiance"
				></el-step>
				<el-step title="步骤3：疑为恶意访问结果列表"
					icon="el-icon-tickets"
				></el-step>
			</el-steps>
			<el-upload class="content" v-if="activeItem == 1"
				drag
				multiple
				accept=".csv, .xlxs, .txt"
				:action="uploadUrl"
				:headers="{'X-CSRFToken': csrfToken}">
				<i class="el-icon-upload"></i>
				<div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
				<div class="el-upload__tip" slot="tip">
					* 仅支持上传txt,xlsx,csv格式文件且名称为“urllog-”加用户标识
					<br> * 文件第一行应为每一列标题，要求为(url，urlArgs，time, application)表示(访问域名，访问参数，访问时间，应用类型)
					<br> * 默认编码格式为GBK 
				</div>
			</el-upload>
			<div class="content" v-if="activeItem == 2" style="width:1100px"> 
				<el-table
					ref="singleTable"
					:data="tableData"
					highlight-current-row
					@current-change="handleCurrentChange">
					<el-table-column label="模型名称">
						<template slot-scope="scope">
								<el-radio v-model="radio" :label="scope.row.name"></el-radio>
						</template>
					</el-table-column>
					<el-table-column property="amount" label="选用数据集大小"></el-table-column>
					<el-table-column property="ratio" label="标注样本比例"></el-table-column>
					<el-table-column property="cv" label="交叉验证折数"></el-table-column>
					<el-table-column property="c1" label="惩罚参数C1"></el-table-column>
					<el-table-column property="c2" label="惩罚参数C2"></el-table-column>
					<el-table-column property="gamma" label="gamma系数"></el-table-column>
					<el-table-column property="date" label="生成日期" width="180"></el-table-column>
				</el-table>
				<el-button type="primary" plain class="page button">开始检测</el-button>
			</div>
			<el-table :data="labelData" v-if="activeItem == 3" class="content">
				<el-table-column prop="user" label="用户标识密文"></el-table-column>
				<el-table-column prop="url" label="Url" width="150"></el-table-column>
				<el-table-column label="访问次数" width="650">
					<template slot-scope="scope">
						<v-chart type="line" :options="scope.row.times"></v-chart>
					</template>
				</el-table-column>
				<el-table-column label="访问参数" width="120">
					<template slot-scope="scope">
						<el-button type="primary" icon="el-icon-view" plain>查看</el-button>
					</template>
				</el-table-column>
			</el-table>
		</el-row>
		<el-pagination class="page" v-if="activeItem != 1"
			background
			layout="prev, pager, next"
			:total="11">
		</el-pagination>
	</div>
</template>

<script>
import $chart from './chart.vue';
import $api from '../io/app.js';
import $cookie from '../util/cookie.js';
export default {
	name: 'check',

	components: {
		'v-chart': $chart
	},

	data() {
		return {
			csrfToken: '', 
			uploadUrl: '/api/upload/url_log',
			radio: '',
			tableData: [{
				name: '模型1',
				amount: 20000,
				ratio: '20%',
				cv: 10,
				c1: 40,
				c2: 10,
				gamma: 0.2,
				date: '2019-01-16 20:56'
			}, {
				name: '模型2',
				amount: 15000,
				ratio: '50%',
				cv: 8,
				c1: 30,
				c2: 1,
				gamma: 0.1,
				date: '2019-01-15 10:03'
			}],
			labelData: [{
				url: '',
				urlArgs: '',
				label: false,
				times: []
			}],
		}
	},
	computed: {
		activeItem() {
			return this.$store.state.step.curStep;
		}
	},
	created() {
		this.$store.dispatch('setStepNum', 3);
		this.csrfToken = $cookie.get('csrftoken');
		this.fetchLabel();
	},
	methods: {
		handleCurrentChange(val) {
			this.radio = val.name;
			this.$refs.singleTable.setCurrentRow(val);
		},
		fetchLabel() {
			let params = {
				page: 1,
				size: 10 
			};
			$api.fetchLabelList(params).then(res => {
				let temp = res.list;
				temp.forEach((element, index) => {
					if (index) {
						element['user'] = 'BzCVEnF2fy1xugsiJBDPmu7ien+8mfMlDvgPtqSCiCe9Qkm6AtldW1DnFRV4zd0v/yPzC7MM+jyUsvd8+ez4N12jqzOSLruP9if7KvkYx7qo99drnU2zrR7Q0WuvPtI+ebc1SGOaD4OmTev9N2kv81nhll2sbRv3l7izJ/WKiO8=';
					} else {
						element['user'] = 'FLBJiInLGD/mcZGD+hLGw0/QVWwOc2JEVRq4EK/vMYxOaBI3aRLd30vYAPjZhL8lMbncGaJQYg2HEzGynQmfEojVO/0NLqxseZ4SMru76shOC95N0uhWBcZwn5jHG9LSSWwIu5/hYuMFnWYNtP6T7VoGbeQqCRBASW/kzPtcEnU=';
					}
				});
				this.labelData = temp;
			});
		},
	}
}
</script>

<style lang="less">
.c-check {
	.left-side {
		font-weight: 800;
    	font-size: 14px;
	}
	.upload-content {
		display: flex;
		margin-top: 10px;
		&.active-1 {
			align-items: center;
		}
		.upload-step {
			height: 500px;
		}
		.content {
			margin-left: 100px;
			.el-button {
				margin-top: 10px;
			}
		}
		.iconfont {
			font-size: 25px;
		}
	}
	.page {
		margin: 5px;
		float: right;
	}
}
</style>

