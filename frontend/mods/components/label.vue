<template>
	<div class="c-label">
		<el-table :data="labelData">
			<el-table-column prop="url" label="Url"></el-table-column>
			<el-table-column width="850" label="访问次数">
				<template slot-scope="scope">
					<v-chart type="line" :options="scope.row.times"></v-chart>
				</template>
			</el-table-column>
			<el-table-column label="访问参数">
				<template slot-scope="scope">
					<el-button type="primary" icon="el-icon-view" @click="handleViewArgs(scope.row.urlArgs)">查看参数列表</el-button>
				</template>
			</el-table-column>
			<el-table-column label="当前标记" align="center">
				<template slot-scope="scope">
					<el-switch v-model="scope.row.label"
						active-text="恶意访问"
						inactive-text="善意访问"
						style="margin-left:5px"></el-switch>
				</template>
			</el-table-column>
		</el-table>
		<el-pagination
		  style="float:right"
		  @size-change="handleSizeChange"
		  @current-change="handlePageChange"
		  :current-page.sync="page"
		  :page-sizes="[10, 20, 50, 100]"
		  :page-size="size"
		  layout="sizes, prev, pager, next"
		  next-text="保存并下一页"
		  @next-click="handleNextClick"
		  :total="logTotal"
		></el-pagination>
		<el-dialog
			title="Url参数"
			width="800"
			:visible.sync="dialogVisible">
			<div style="word-break:break-word">{{ dialogText.slice(1, -1).split(',').join('\n\n') }}</div>
			<span slot="footer" class="dialog-footer">
				<el-button @click="dialogVisible = false">取 消</el-button>
				<el-button type="primary" @click="dialogVisible = false">确 定</el-button>
			</span>
		</el-dialog>
	</div>
</template>

<script>
import $chart from './chart.vue';
import $api from '../io/app.js';
export default {
	name: 'data-label',

	components: {
		'v-chart': $chart
	},

	data() {
		return {
			labelData: [{
				url: '',
				urlArgs: '',
				label: false,
				times: []
			}],
			logTotal: 0,
			size: 10,
			page: 1,
			dialogVisible: false,
			dialogText: ''
		}
	},

	created() {
		this.fetchLabel();
		this.$store.dispatch('setStepNum', 0);
	},

	methods: {
		fetchLabel() {
			let params = {
				page: this.page,
				size: this.size
			};
			$api.fetchLabelList(params).then(res => {
				let temp = res.list;
				temp.forEach(element => {
					element['label'] = false;
				});
				this.labelData = temp;
				this.logTotal = res.total;
			});
		},
		handleSizeChange(val) {
			this.size = val;
			this.page = 1;
			this.fetchLabel();
		},
		handlePageChange() {
			this.fetchLabel();
		},
		handleViewArgs(args) {
			this.dialogText = args;
			this.dialogVisible = true;
		},
		handleNextClick(){
			$api.saveLabel({label: this.labelData}).then(res => {
				if (res == 'ok') {
					this.$message('标记成功, 请开始第' + this.page + '页');
				}
			});
		}
	}
}
</script>

