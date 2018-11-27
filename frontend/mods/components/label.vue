<template>
	<div class="c-label">
		<el-table :data="labelData">
			<el-table-column prop="url" label="Url"></el-table-column>
			<el-table-column prop="urlArgs" label="参数列表"></el-table-column>
			<el-table-column label="访问次数">
				<template slot-scope="scope">
					<v-chart type="line" :title="scope.row.url" :options="scope.row.options"></v-chart>
				</template>
			</el-table-column>
			<el-table-column label="标记">
				<template slot-scope="scope">
					<el-switch v-model="scope.row.label"></el-switch>
				</template>
			</el-table-column>
		</el-table>
	</div>
</template>

<script>
import $chart from './chart.vue';
export default {
	name: 'data-label',

	components: {
		'v-chart': $chart
	},

	data() {
		return {
			labelData: [
				{
					url: 'test',
					urlArgs: [1, 2],
					label: false,
					options: {
						first: 2,
						second: 3
					}
				}
			]
		}
	}
}
</script>

