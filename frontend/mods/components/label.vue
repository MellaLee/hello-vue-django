<template>
	<div class="c-label">
		<el-table :data="labelData">
			<el-table-column prop="url" label="Url"></el-table-column>
			<el-table-column width="650" label="访问次数">
				<template slot-scope="scope">
					<v-chart type="line" :options="scope.row.times"></v-chart>
				</template>
			</el-table-column>
			<el-table-column label="标记">
				<template slot-scope="scope">
					<el-switch v-model="scope.row.label"></el-switch>
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
		  :total="logTotal"
		></el-pagination>
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
				label: false,
				times: []
			}],
			logTotal: 0,
			size: 10,
			page: 1
		}
	},

	created() {
		this.fetchLabel();
	},

	methods: {
		fetchLabel() {
			let params = {
				page: this.page,
				size: this.size
			};
			$api.fetchLabelList(params).then(res => {
				this.labelData = res.list;
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
		}
	}
}
</script>

