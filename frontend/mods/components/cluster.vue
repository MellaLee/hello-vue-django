<template>
	<div class="c-cluster">
		<i class="cluster-title iconfont icon-tiao"></i>聚类标记
		<div class="cluster-content">
			<el-steps class="cluster-step" direction="vertical" :active="activeItem">
				<el-step title="步骤1：聚类"
					description="初步划分样本类别"
					icon="iconfont icon-julei"
				></el-step>
				<el-step title="步骤2：查看聚类结果"
					description="展示聚类结果分布图、准确率等"
					icon="el-icon-document"
				></el-step>
			</el-steps>
			<div class="cluster-step-content">
				<el-button v-if="activeItem == 1" type="primary" :loading="clusterStatus == 'ing'" plain round>
					{{ clusterStatusDict[clusterStatus] }}
				</el-button>
				<el-button v-if="activeItem == 1" type="info" :loading="true" plain round>
					聚类中
				</el-button>
				<el-button v-if="activeItem == 1" type="success" plain round>
					上次聚类完成，重新聚类
				</el-button>
				<div class="cluster-result" v-else>
					<el-carousel class="carousel" indicator-position="outside" :autoplay="false" height="600px">
						<el-carousel-item v-for="item in clusterResult" :key="item">
							<h3><img :src="item"></h3>
						</el-carousel-item>
					</el-carousel>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'cluster',
	data() {
		return {
			clusterStatusDict: {
				start: '开始聚类',
				ing: '聚类中',
				end: '聚类完成'
			},
			clusterStatus: 'start',
			clusterResult: [
				'static/image/cluster/diag.png',
				"static/image/cluster/full.png",
				"static/image/cluster/tied.png",
				"static/image/cluster/spherical.png"
			]
		};
	},
	computed: {
		activeItem() {
			return this.$store.state.step.curStep;
		}
	},
	created() {
		this.$store.dispatch('setStepNum', 2);
	}
}
</script>

<style lang="less">
.c-cluster {
	.cluster-content {
		display: flex;
		align-items: center;
		.cluster-step {
			height: 200px;
			margin-top: 5px;
			.iconfont {
				font-size: 25px;
			}
		}
		.cluster-result {
			.carousel {
				width: 1300px;
				img {
					width: 1300px;
				}
			}
		}
	}
}
</style>
