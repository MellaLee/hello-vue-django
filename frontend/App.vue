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
							<el-container>
								<el-main>
									<div v-if="active === 0">
										<v-upload-log></v-upload-log>	
									</div>
									<div v-else-if="active === 1">
										<v-url-list></v-url-list>	
									</div>
									<div v-else-if="active === 2">
										<v-label></v-label>	
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
import $uploadLog from './mods/components/uploadLog.vue';
import $urlList from './mods/components/urlList.vue';
import $label from './mods/components/label.vue';

export default {
	name: 'app',
	data() {
		return {
			active: 0,
			stepName: [
				{ title: '数据获取', description: '获取与清洗日志' }, 
				{ title: '特征提取', description: '提取并量化特征'}, 
				{ title: '数据标记', description: '人工标记'},
				{ title: '半监督学习', description: '上传未标记训练集合并进行预测'}],
		}
	},

	components: {
		'v-upload-log': $uploadLog,
		'v-url-list': $urlList,
		'v-label': $label
	},

	methods: {
		back(index) {
			if (this.active-- < 0) this.active = 0;
		},
		nextStep(index) {
			this.active ++;
			if (this.active > 2) {
				this.active = 0;
			}
		}
	},
}
</script>

<style>
</style>
