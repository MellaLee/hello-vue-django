<template>
	<div class="c-navside">
		<el-menu
			default-active="upload"
			background-color="#272727"
			text-color="#9d9d9d"
			active-text-color="#fff"
			router
			class="navside-menu">
			<el-submenu index="train">
				<template slot="title">
					<img class="normal logo" src="static/image/train.png">
					<span>检测模型训练子平台</span>
				</template>
				<el-menu-item-group>
					<el-menu-item v-for="item in trainNav" :index="item.path" :key="item.name">
						<img class="xs logo" :src="'static/image/'+item.name + '.png'">
						{{ item.text }}
					</el-menu-item>
				</el-menu-item-group>
			</el-submenu>
			<el-submenu index="2">
				<template slot="title">
					<img class="normal logo" src="static/image/test.png">
					<span>恶意访问识别子平台</span>
				</template>
				<el-menu-item-group>
					<el-menu-item index="/identify/check">
						<img class="xs logo" src="static/image/check.png">
						恶意检测
					</el-menu-item>
				</el-menu-item-group>
			</el-submenu>
		</el-menu>
	</div>
</template>

<script>
export default {
	name: 'navSide',
	data() {
		return {
			trainNav: [{
				text: '数据获取',
				path: '/train/upload',
				name: 'upload'
			}, {
				text: '特征提取',
				path: '/train/feature',
				name: 'feature'
			}, {
				text: '聚类标记',
				path: '/train/cluster',
				name: 'cluster'
			}, {
				text: '半监督学习',
				path: '/train/semiSupervised',
				name: 'semiSupervised'
			}] 
		}
	}
}
</script>


<style lang="less">
.c-navside {
	.navside-menu {
		bottom: 0;
		left: 0;
		top: 60px;
		position: fixed;
		width: 280px;
		.logo {
			margin-right: 0.5rem;
		}
		.normal.logo {
			width: 28px;
		}
		.xs.logo {
			width: 26px;
		}
	}
}
</style>
