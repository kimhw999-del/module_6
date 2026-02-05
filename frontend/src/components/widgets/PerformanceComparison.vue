<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { etfApi } from '@/services/api'
import type { ETF } from '@/types'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const etfs = ref<ETF[]>([])
const selectedETFs = ref<string[]>([])
const loading = ref(false)
const searchQuery = ref('')
const filterSector = ref<string>('all')
const viewMode = ref<'chart' | 'table'>('chart')
const period = ref<'1d' | '1w' | '1m' | '1y'>('1y')

const colors = [
  'rgba(255, 99, 132, 1)',
  'rgba(54, 162, 235, 1)',
  'rgba(255, 206, 86, 1)',
  'rgba(75, 192, 192, 1)',
  'rgba(153, 102, 255, 1)',
  'rgba(255, 159, 64, 1)',
  'rgba(201, 203, 207, 1)',
  'rgba(83, 102, 255, 1)',
]

// 필터링된 ETF 목록
const filteredETFs = computed(() => {
  let result = etfs.value

  // 검색 필터
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(e =>
      e.ticker.toLowerCase().includes(query) ||
      e.name.toLowerCase().includes(query)
    )
  }

  // 섹터 필터
  if (filterSector.value !== 'all') {
    result = result.filter(e => e.sector === filterSector.value)
  }

  return result
})

// 섹터 목록
const sectors = computed(() => {
  const uniqueSectors = [...new Set(etfs.value.map(e => e.sector))]
  return uniqueSectors.sort()
})

const chartData = computed(() => {
  const selected = etfs.value.filter(e => selectedETFs.value.includes(e.ticker))

  return {
    labels: ['일간', '주간', '월간', '연간'],
    datasets: selected.map((etf, index) => ({
      label: `${etf.ticker} - ${etf.name}`,
      data: [etf.return_1d, etf.return_1w, etf.return_1m, etf.return_1y],
      borderColor: colors[index % colors.length],
      backgroundColor: colors[index % colors.length].replace('1)', '0.2)'),
      tension: 0.3,
      borderWidth: 3,
      pointRadius: 5,
      pointHoverRadius: 8,
    }))
  }
})

// 테이블 데이터
const tableData = computed(() => {
  return etfs.value
    .filter(e => selectedETFs.value.includes(e.ticker))
    .map(etf => ({
      ticker: etf.ticker,
      name: etf.name,
      return_1d: etf.return_1d,
      return_1w: etf.return_1w,
      return_1m: etf.return_1m,
      return_1y: etf.return_1y,
      dividend_yield: etf.dividend_yield,
    }))
})

// 평균 수익률 계산
const averageReturns = computed(() => {
  if (selectedETFs.value.length === 0) return null

  const selected = etfs.value.filter(e => selectedETFs.value.includes(e.ticker))
  return {
    avg_1d: (selected.reduce((sum, e) => sum + e.return_1d, 0) / selected.length).toFixed(2),
    avg_1w: (selected.reduce((sum, e) => sum + e.return_1w, 0) / selected.length).toFixed(2),
    avg_1m: (selected.reduce((sum, e) => sum + e.return_1m, 0) / selected.length).toFixed(2),
    avg_1y: (selected.reduce((sum, e) => sum + e.return_1y, 0) / selected.length).toFixed(2),
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index' as const,
    intersect: false,
  },
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        padding: 15,
        font: { size: 11 },
        usePointStyle: true,
      }
    },
    title: {
      display: false,
    },
    tooltip: {
      callbacks: {
        label: function(context: any) {
          return `${context.dataset.label}: ${context.parsed.y.toFixed(2)}%`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: false,
      ticks: {
        callback: function(value: any) {
          return value + '%'
        }
      },
      grid: {
        color: 'rgba(0, 0, 0, 0.05)',
      }
    },
    x: {
      grid: {
        display: false,
      }
    }
  }
}

const fetchETFs = async () => {
  loading.value = true
  try {
    const response = await etfApi.getAll()
    etfs.value = response.data
    // 기본으로 높은 배당률 순으로 3개 선택
    const topDividend = [...response.data]
      .sort((a, b) => b.dividend_yield - a.dividend_yield)
      .slice(0, 3)
    selectedETFs.value = topDividend.map(e => e.ticker)
  } catch (error) {
    console.error('ETF 목록 조회 실패:', error)
  } finally {
    loading.value = false
  }
}

const toggleETF = (ticker: string) => {
  const index = selectedETFs.value.indexOf(ticker)
  if (index > -1) {
    selectedETFs.value.splice(index, 1)
  } else {
    if (selectedETFs.value.length < 8) {
      selectedETFs.value.push(ticker)
    }
  }
}

const clearSelection = () => {
  selectedETFs.value = []
}

const selectTopDividend = () => {
  const top = [...etfs.value]
    .sort((a, b) => b.dividend_yield - a.dividend_yield)
    .slice(0, 5)
  selectedETFs.value = top.map(e => e.ticker)
}

const selectTopReturn = () => {
  const top = [...etfs.value]
    .sort((a, b) => b.return_1y - a.return_1y)
    .slice(0, 5)
  selectedETFs.value = top.map(e => e.ticker)
}

const formatPercent = (value: number) => {
  const color = value >= 0 ? 'success' : 'error'
  const sign = value >= 0 ? '+' : ''
  return { text: `${sign}${value.toFixed(2)}%`, color }
}

onMounted(() => {
  fetchETFs()
})
</script>

<template>
  <v-card>
    <v-card-title class="d-flex justify-space-between align-center">
      <div>
        <span class="text-h5">ETF 성과 비교</span>
        <v-chip class="ml-3" color="primary" size="small">
          {{ selectedETFs.length }}개 선택
        </v-chip>
      </div>
      <v-btn-toggle v-model="viewMode" mandatory density="compact" variant="outlined">
        <v-btn value="chart" size="small">
          <v-icon>mdi-chart-line</v-icon>
        </v-btn>
        <v-btn value="table" size="small">
          <v-icon>mdi-table</v-icon>
        </v-btn>
      </v-btn-toggle>
    </v-card-title>

    <v-card-text>
      <div v-if="loading" class="text-center py-8">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <div class="text-caption mt-2">ETF 데이터 로딩 중...</div>
      </div>

      <div v-else>
        <!-- 빠른 선택 버튼 -->
        <div class="mb-4">
          <div class="text-subtitle-2 mb-2">빠른 선택</div>
          <v-btn-group density="compact" variant="outlined">
            <v-btn @click="selectTopDividend" size="small">
              <v-icon start>mdi-cash-multiple</v-icon>
              높은 배당률 TOP 5
            </v-btn>
            <v-btn @click="selectTopReturn" size="small">
              <v-icon start>mdi-trending-up</v-icon>
              높은 수익률 TOP 5
            </v-btn>
            <v-btn @click="clearSelection" size="small" color="error" variant="text">
              <v-icon start>mdi-close</v-icon>
              초기화
            </v-btn>
          </v-btn-group>
        </div>

        <!-- 검색 및 필터 -->
        <v-row dense class="mb-4">
          <v-col cols="12" md="8">
            <v-text-field
              v-model="searchQuery"
              density="compact"
              placeholder="ETF 검색 (티커, 이름)"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              hide-details
              clearable
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              v-model="filterSector"
              :items="[{ title: '전체 섹터', value: 'all' }, ...sectors.map(s => ({ title: s, value: s }))]"
              density="compact"
              variant="outlined"
              hide-details
            ></v-select>
          </v-col>
        </v-row>

        <!-- ETF 선택 칩 -->
        <div class="mb-4" style="max-height: 200px; overflow-y: auto;">
          <div class="text-caption text-grey mb-2">
            비교할 ETF 선택 (최대 8개) - 클릭하여 선택/해제
          </div>
          <v-chip-group column>
            <v-chip
              v-for="etf in filteredETFs"
              :key="etf.ticker"
              :color="selectedETFs.includes(etf.ticker) ? 'primary' : 'default'"
              :variant="selectedETFs.includes(etf.ticker) ? 'flat' : 'outlined'"
              size="small"
              @click="toggleETF(etf.ticker)"
              class="ma-1"
            >
              <v-icon v-if="selectedETFs.includes(etf.ticker)" start size="small">mdi-check</v-icon>
              {{ etf.ticker }}
              <span class="text-caption ml-2 text-grey">{{ etf.dividend_yield.toFixed(1) }}%</span>
            </v-chip>
          </v-chip-group>
        </div>

        <v-divider class="my-4"></v-divider>

        <!-- 선택 없음 -->
        <div v-if="selectedETFs.length === 0" class="text-center py-8">
          <v-icon size="64" color="grey-lighten-1">mdi-chart-line-variant</v-icon>
          <div class="text-h6 text-grey mt-3">비교할 ETF를 선택하세요</div>
          <div class="text-caption text-grey">위의 칩을 클릭하여 최대 8개까지 선택 가능</div>
        </div>

        <!-- 차트 뷰 -->
        <div v-else-if="viewMode === 'chart'">
          <div style="height: 400px" class="mb-4">
            <Line :data="chartData" :options="chartOptions" />
          </div>

          <!-- 평균 수익률 -->
          <v-card variant="tonal" color="info" class="mb-4" v-if="averageReturns">
            <v-card-text>
              <div class="text-subtitle-2 mb-3">
                <v-icon start>mdi-calculator</v-icon>
                평균 수익률 ({{ selectedETFs.length }}개 ETF)
              </div>
              <v-row dense>
                <v-col cols="3">
                  <div class="text-caption text-grey">일간</div>
                  <div class="text-h6">{{ averageReturns.avg_1d }}%</div>
                </v-col>
                <v-col cols="3">
                  <div class="text-caption text-grey">주간</div>
                  <div class="text-h6">{{ averageReturns.avg_1w }}%</div>
                </v-col>
                <v-col cols="3">
                  <div class="text-caption text-grey">월간</div>
                  <div class="text-h6">{{ averageReturns.avg_1m }}%</div>
                </v-col>
                <v-col cols="3">
                  <div class="text-caption text-grey">연간</div>
                  <div class="text-h6 text-primary">{{ averageReturns.avg_1y }}%</div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- 선택된 ETF 리스트 -->
          <div class="text-subtitle-2 mb-2">선택된 ETF 상세</div>
          <v-list density="compact">
            <v-list-item
              v-for="etf in etfs.filter(e => selectedETFs.includes(e.ticker))"
              :key="etf.ticker"
            >
              <template v-slot:prepend>
                <v-chip size="small" :color="colors[selectedETFs.indexOf(etf.ticker) % colors.length]" variant="flat">
                  {{ etf.ticker }}
                </v-chip>
              </template>

              <v-list-item-title>{{ etf.name }}</v-list-item-title>
              <v-list-item-subtitle>
                배당: {{ etf.dividend_yield.toFixed(2) }}% | 섹터: {{ etf.sector }}
              </v-list-item-subtitle>

              <template v-slot:append>
                <div class="text-right">
                  <div class="text-caption text-grey">연간 수익률</div>
                  <v-chip
                    :color="formatPercent(etf.return_1y).color"
                    size="small"
                    variant="flat"
                  >
                    {{ formatPercent(etf.return_1y).text }}
                  </v-chip>
                </div>
              </template>
            </v-list-item>
          </v-list>
        </div>

        <!-- 테이블 뷰 -->
        <div v-else-if="viewMode === 'table'">
          <v-table density="compact">
            <thead>
              <tr>
                <th>티커</th>
                <th>이름</th>
                <th class="text-right">일간</th>
                <th class="text-right">주간</th>
                <th class="text-right">월간</th>
                <th class="text-right">연간</th>
                <th class="text-right">배당률</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in tableData" :key="item.ticker">
                <td>
                  <v-chip size="small" color="primary" variant="outlined">
                    {{ item.ticker }}
                  </v-chip>
                </td>
                <td>{{ item.name }}</td>
                <td class="text-right">
                  <v-chip
                    :color="formatPercent(item.return_1d).color"
                    size="x-small"
                    variant="tonal"
                  >
                    {{ formatPercent(item.return_1d).text }}
                  </v-chip>
                </td>
                <td class="text-right">
                  <v-chip
                    :color="formatPercent(item.return_1w).color"
                    size="x-small"
                    variant="tonal"
                  >
                    {{ formatPercent(item.return_1w).text }}
                  </v-chip>
                </td>
                <td class="text-right">
                  <v-chip
                    :color="formatPercent(item.return_1m).color"
                    size="x-small"
                    variant="tonal"
                  >
                    {{ formatPercent(item.return_1m).text }}
                  </v-chip>
                </td>
                <td class="text-right">
                  <v-chip
                    :color="formatPercent(item.return_1y).color"
                    size="small"
                    variant="flat"
                  >
                    {{ formatPercent(item.return_1y).text }}
                  </v-chip>
                </td>
                <td class="text-right font-weight-bold">
                  {{ item.dividend_yield.toFixed(2) }}%
                </td>
              </tr>
            </tbody>
          </v-table>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.text-green {
  color: #4caf50;
}

.text-red {
  color: #f44336;
}
</style>
