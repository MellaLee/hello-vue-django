<template>
	<div id="app">
		<el-row>
			<el-col :span="18" :offset="3">
				<el-container style="border: 1px solid #eee">
					<el-header>
						<h3 style="text-align: center">URL恶意访问识别系统</h3>
					</el-header>

					<el-main>
						<el-steps :active="active" finish-status="success" align-center>
							<el-step v-for="(obj, index) in stepName" :key="index" :title="obj.title" :description="obj.description"></el-step>
						</el-steps>

						<el-card style="margin-top:12px">
							<el-container style="height:400px">
								<el-main>
									<div v-if="active === 0">
										<el-upload drag :action="uploadUrl" multiple :headers="{'X-CSRFToken': csrfToken}">
											<i class="el-icon-upload"></i>
											<div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
											<div class="el-upload__tip" slot="tip">
												* 目的: 以用户为单位，将其该段时间内的访问数据集存入MySQL表sys_urllog
												<br/>
												* 仅支持上传CSV文件
											</div>
										</el-upload>
									</div>
									<div v-else-if="active === 1">
										<el-table :data="tableData">
											<el-table-column prop="user_id" label="用户"></el-table-column>
											<el-table-column prop="url" label="访问域名"></el-table-column>
											<el-table-column prop="similarEuc" label="特征D"></el-table-column>
											<el-table-column prop="urlArgsEntropy" label="特征H"></el-table-column>
											<el-table-column prop="abnormalTimeProbability" label="特征Ptime"></el-table-column>
											<el-table-column prop="sameArgsDiversity" label="特征Puri"></el-table-column>
											<el-table-column prop="webClassify" label="特征Cweb"></el-table-column>
										</el-table>
										<el-pagination layout="prev, pager, next" :total="129454"></el-pagination>
									</div>
								</el-main>
								<el-footer>
									<el-button-group style="float:right">
										<el-button :disabled="!active" icon="el-icon-arrow-left" style="margin: 12px 1px" type="primary" @click="back">上一步</el-button>
										<el-button :disabled="active == 3" style="margin: 12px 1px" type="primary" @click="nextStep">
											下一步<i class="el-icon-arrow-right el-icon--right"></i>
										</el-button>
									</el-button-group>
								</el-footer>
								</el-container>
						</el-card>
					</el-main>
				</el-container>
			</el-col>
		</el-row>
	</div>
</template>

<script>
export default {
	name: 'app',
	data () {
		return {
			active: 0,
			stepName: [
				{ title: '数据获取', description: '获取与清洗日志' }, 
				{ title: '特征提取', description: '提取并量化特征'}, 
				{ title: '聚类标记', description: '聚类标记'},
				{ title: '半监督学习', description: '上传未标记训练集合并进行预测'}],
			uploadUrl: '/api/upload/url_log',
			csrfToken: '', 
			tableData:[
				{
					url: '111.161.111.177',
					similarEuc: 12,
					urlArgsEntropy: 0.376770161256437,
					abnormalTimeProbability: 0,
					sameArgsDiversity: 0,
					webClassify: 0.25,
					user_id: 1
				}, {
					url: 'stat.funshion.net',
					similarEuc: 294,
					urlArgsEntropy: 4.1846774567742,
					abnormalTimeProbability: 1.59391195052098,
					sameArgsDiversity: 0.1781,
					webClassify: 1,
					user_id: 1
				}, {
					url: 'short.weixin.qq.com',
					similarEuc: 103,
					urlArgsEntropy: 1.14383363728164,
					abnormalTimeProbability: 1.28197512425571e-16,
					sameArgsDiversity: 0,
					webClassify: 1,
					user_id: 1
				}, {
					url: 'stat.sd.360.cn',
					similarEuc: 7,
					urlArgsEntropy: 0.693147180559945,
					abnormalTimeProbability: 0,
					sameArgsDiversity: 0,
					webClassify: 1,
					user_id: 1
				}, {
					url: 'get.sougou.com',
					similarEuc: 286,
					urlArgsEntropy: 0,
					abnormalTimeProbability: 0,
					sameArgsDiversity: 0,
					webClassify: 1,
					user_id: 1
				}
			]
		}
	},

	created() {
		this.csrfToken = this.getCookie('csrftoken');
	},

	methods: {
		back(index) {
			if (this.active-- < 0) this.active = 0;
		},
		nextStep(index) {
			if (this.active++ > 2) this.active = 0;
		},
		getCookie(name) {
			let arr,
				reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)")
			if (arr = document.cookie.match(reg)) {
				return decodeURIComponent(arr[2])
			}
		},
	},
}
</script>

<style>
</style>
