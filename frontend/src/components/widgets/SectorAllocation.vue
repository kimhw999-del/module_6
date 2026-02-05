<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { etfApi } from '@/services/api'
import type { SectorAllocation, RegionAllocation } from '@/types'

ChartJS.register(ArcElement, Tooltip, Legend)

const viewType = ref<'sector' | 'region'>('sector')
const sectorData = ref<SectorAllocation>({})
const regionData = ref<RegionAllocation>({})
const loading = ref(false)
const showPercentage = ref(true)

const colors = [
  '#FF6384',
  '#36A2EB',
  '#FFCE56',
  '#4BC0C0',
  '#9966FF',
  '#FF9F40',
  '#C9CBCF',
  '#5366FF',
  '#FF6B9D',
  '#36EB9F',
]

const chartData = computed(() => {
  const data = viewType.value === 'sector' ? sectorData.value : regionData.value
  const labels = Object.keys(data)
  const values = Object.values(data)

  return {
    labels,
    datasets: [
      {
        data: values,
        backgroundColor: colors.slice(0, labels.length),
        borderWidth: 3,
        borderColor: '#fff',
        hoverOffset: 15,
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '60%',
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        padding: 15,
        font: { size: 11 },
        usePointStyle: true,
        generateLabels: function(chart: any) {
          const data = chart.data
          if (data.labels.length && data.datasets.length) {
            const total = data.datasets[0].data.reduce((a: number, b: number) => a + b, 0)
            return data.labels.map((label: string, i: number) => {
              const value = data.datasets[0].data[i]
              const percentage = ((value / total) * 100).toFixed(1)
              return {
                text: `${label} (${percentage}%)`,
                fillStyle: data.datasets[0].backgroundColor[i],
                hidden: false,
                index: i
              }
            })
          }
          return []
        }
      }
    },
    tooltip: {
      callbacks: {
        label: function(context: any) {
          const label = context.label || ''
          const value = context.parsed || 0
          const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0)
          const percentage = ((value / total) * 100).toFixed(1)
          return `${label}: ${value}개 (${percentage}%)`
        }
      }
    }
  }
}

// 통계 계산
const statistics = computed(() => {
  const data = viewType.value === 'sector' ? sectorData.value : regionData.value
  const entries = Object.entries(data)
  const total = Object.values(data).reduce((sum, val) => sum + val, 0)

  if (entries.length === 0) return null

  const sorted = entries.sort((a, b) => b[1] - a[1])
  const top = sorted[0]

  return {
    total,
    categories: entries.length,
    topCategory: top[0],
    topCount: top[1],
    topPercentage: ((top[1] / total) * 100).toFixed(1)
  }
})

// 정렬된 데이터
const sortedData = computed(() => {
  const data = viewType.value === 'sector' ? sectorData.value : regionData.value
  const entries = Object.entries(data)
  return entries.sort((a, b) => b[1] - a[1])
})

// 비율 계산
const getPercentage = (value: number) => {
  const data = viewType.value === 'sector' ? sectorData.value : regionData.value
  const total = Object.values(data).reduce((sum, val) => sum + val, 0)
  return ((value / total) * 100).toFixed(1)
}

const fetchAllocations = async () => {
  loading.value = true
  try {
    const [sectorResponse, regionResponse] = await Promise.all([
      etfApi.getSectorAllocation(),
      etfApi.getRegionAllocation()
    ])
    sectorData.value = sectorResponse.data
    regionData.value = regionResponse.data
  } catch (error) {
    console.error('분산도 조회 실패:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAllocations()
})
</script>

<template>
  <v-card>
    <v-card-title class="d-flex justify-space-between align-center">
      <div>
        <v-icon class="mr-2">mdi-chart-donut</v-icon>
        {{ viewType === 'sector' ? '섹터' : '지역' }} 분산도
      </div>
      <v-btn-toggle v-model="viewType" density="compact" mandatory variant="outlined">
        <v-btn value="sector" size="small">
          <v-icon start>mdi-factory</v-icon>
          섹터
        </v-btn>
        <v-btn value="region" size="small">
          <v-icon start>mdi-earth</v-icon>
          지역
        </v-btn>
      </v-btn-toggle>
    </v-card-title>

    <v-card-text>
      <div v-if="loading" class="text-center py-8">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <div class="text-caption mt-2">분산도 계산 중...</div>
      </div>

      <div v-else>
        <!-- 통계 카드 -->
        <v-card v-if="statistics" variant="tonal" color="info" class="mb-4">
          <v-card-text>
            <v-row dense>
              <v-col cols="4">
                <div class="text-caption text-grey">총 ETF</div>
                <div class="text-h6">{{ statistics.total }}개</div>
              </v-col>
              <v-col cols="4">
                <div class="text-caption text-grey">카테고리</div>
                <div class="text-h6">{{ statistics.categories }}개</div>
              </v-col>
              <v-col cols="4">
                <div class="text-caption text-grey">최대 비중</div>
                <div class="text-h6">{{ statistics.topPercentage }}%</div>
              </v-col>
            </v-row>
            <v-divider class="my-2"></v-divider>
            <div class="text-caption">
              <v-icon size="small" class="mr-1">mdi-crown</v-icon>
              <span class="font-weight-bold">{{ statistics.topCategory }}</span>
              섹터가 {{ statistics.topCount }}개로 가장 많습니다
            </div>
          </v-card-text>
        </v-card>

        <!-- 도넛 차트 -->
        <div style="height: 400px" class="position-relative">
          <Doughnut :data="chartData" :options="chartOptions" />

          <!-- 중앙 텍스트 -->
          <div
            style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; pointer-events: none;"
          >
            <div class="text-h4 font-weight-bold">{{ statistics?.total }}</div>
            <div class="text-caption text-grey">Total ETFs</div>
          </div>
        </div>

        <v-divider class="my-4"></v-divider>

        <!-- 상세 리스트 -->
        <div class="d-flex justify-space-between align-center mb-3">
          <div class="text-subtitle-2">상세 분포</div>
          <v-btn-toggle v-model="showPercentage" density="compact" variant="outlined">
            <v-btn :value="false" size="x-small">개수</v-btn>
            <v-btn :value="true" size="x-small">비율</v-btn>
          </v-btn-toggle>
        </div>

        <v-list density="compact">
          <v-list-item
            v-for="([key, value], index) in sortedData"
            :key="key"
            class="mb-1"
          >
            <template v-slot:prepend>
              <v-icon
                :color="colors[index % colors.length]"
                size="small"
              >
                mdi-circle
              </v-icon>
            </template>

            <v-list-item-title class="font-weight-medium">{{ key }}</v-list-item-title>

            <template v-slot:append>
              <div class="d-flex align-center ga-2">
                <v-progress-linear
                  :model-value="parseFloat(getPercentage(value))"
                  :color="colors[index % colors.length]"
                  height="6"
                  rounded
                  style="width: 80px;"
                ></v-progress-linear>
                <v-chip
                  size="small"
                  :color="colors[index % colors.length]"
                  variant="flat"
                >
                  {{ showPercentage ? `${getPercentage(value)}%` : `${value}개` }}
                </v-chip>
              </div>
            </template>
          </v-list-item>
        </v-list>

        <!-- 다양성 지표 -->
        <v-card variant="outlined" class="mt-4">
          <v-card-text>
            <div class="text-caption text-grey mb-2">
              <v-icon size="small" class="mr-1">mdi-information</v-icon>
              포트폴리오 다양성
            </div>
            <div class="text-body-2">
              {{ statistics?.categories }}개의 {{ viewType === 'sector' ? '섹터' : '지역' }}에
              분산 투자되어 있습니다.
              <span v-if="statistics && statistics.categories >= 5" class="text-success font-weight-bold">
                우수한 분산도
              </span>
              <span v-else-if="statistics && statistics.categories >= 3" class="text-info font-weight-bold">
                적정한 분산도
              </span>
              <span v-else class="text-warning font-weight-bold">
                낮은 분산도
              </span>
            </div>
          </v-card-text>
        </v-card>
      </div>
    </v-card-text>
  </v-card>
</template>
