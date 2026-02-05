<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Line, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler,
  ArcElement,
  Legend
} from 'chart.js'
import { etfApi } from '@/services/api'
import type { ETF } from '@/types'

// Chart.js 등록
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler,
  ArcElement,
  Legend
)

const etfs = ref<ETF[]>([])
const loading = ref(false)
const search = ref('')
const error = ref('')
const columnDialog = ref(false)
const detailDialog = ref(false)
const selectedETF = ref<ETF | null>(null)

// 모든 컬럼 정의
const allHeaders = [
  { title: '티커', key: 'ticker', align: 'start' as const, sortable: true, required: true },
  { title: '이름', key: 'name', align: 'start' as const, sortable: true, required: true },
  { title: '가격 추이', key: 'price_chart', align: 'center' as const, sortable: false },
  { title: '현재가', key: 'current_price', align: 'end' as const, sortable: true },
  { title: '배당수익률', key: 'dividend_yield', align: 'end' as const, sortable: true },
  { title: '일간', key: 'return_1d', align: 'end' as const, sortable: true },
  { title: '주간', key: 'return_1w', align: 'end' as const, sortable: true },
  { title: '월간', key: 'return_1m', align: 'end' as const, sortable: true },
  { title: '연간', key: 'return_1y', align: 'end' as const, sortable: true },
  { title: '섹터', key: 'sector', align: 'start' as const, sortable: true },
  { title: '지역', key: 'region', align: 'start' as const, sortable: true },
  { title: '비용비율', key: 'expense_ratio', align: 'end' as const, sortable: true },
  { title: '운용자산(억)', key: 'aum', align: 'end' as const, sortable: true },
]

// 선택된 컬럼 (localStorage에서 불러오기)
const selectedColumns = ref<string[]>([])

// 초기 선택 컬럼 설정
const initializeColumns = () => {
  const saved = localStorage.getItem('etf-table-columns')
  if (saved) {
    selectedColumns.value = JSON.parse(saved)
  } else {
    // 기본 컬럼 선택
    selectedColumns.value = ['ticker', 'name', 'price_chart', 'current_price', 'dividend_yield', 'return_1w', 'return_1m', 'sector']
  }
}

// 컬럼 저장
const saveColumns = () => {
  localStorage.setItem('etf-table-columns', JSON.stringify(selectedColumns.value))
  columnDialog.value = false
}

// 표시할 헤더 필터링
const headers = computed(() => {
  return allHeaders.filter(h => selectedColumns.value.includes(h.key))
})

const fetchETFs = async () => {
  loading.value = true
  error.value = ''
  try {
    console.log('API 호출 시작: /api/etfs')
    const response = await etfApi.getAll()
    console.log('API 응답:', response)
    etfs.value = response.data
    console.log('ETF 데이터 로드 완료:', etfs.value.length, '개')
  } catch (err: any) {
    console.error('ETF 데이터 조회 실패:', err)
    error.value = err.message || String(err)
    if (err.response) {
      console.error('응답 상태:', err.response.status)
      console.error('응답 데이터:', err.response.data)
    }
  } finally {
    loading.value = false
  }
}

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0
  }).format(value)
}

const formatPercent = (value: number) => {
  const color = value >= 0 ? 'success' : 'error'
  const sign = value >= 0 ? '+' : ''
  return { text: `${sign}${value.toFixed(2)}%`, color }
}

const getYieldColor = (yield_value: number) => {
  if (yield_value >= 8) return 'success'
  if (yield_value >= 5) return 'info'
  if (yield_value >= 3) return 'warning'
  return 'default'
}

// 1주일치 가격 데이터 생성 (실제로는 백엔드에서 가져와야 함)
const generateWeeklyPrices = (etf: ETF) => {
  const prices = []
  const currentPrice = etf.current_price
  const weeklyReturn = etf.return_1w / 100
  const startPrice = currentPrice / (1 + weeklyReturn)

  // 7일간의 가격 생성 (시작가에서 현재가까지 점진적 변화)
  for (let i = 0; i < 7; i++) {
    const ratio = i / 6
    const price = startPrice + (currentPrice - startPrice) * ratio
    // 약간의 랜덤 변동 추가
    const randomFactor = 1 + (Math.random() - 0.5) * 0.02
    prices.push(price * randomFactor)
  }

  return prices
}

// 미니 차트 옵션
const getMiniChartOptions = (etf: ETF) => {
  const prices = generateWeeklyPrices(etf)
  const color = etf.return_1w >= 0 ? 'rgb(76, 175, 80)' : 'rgb(244, 67, 54)'

  return {
    labels: ['월', '화', '수', '목', '금', '토', '일'],
    datasets: [
      {
        data: prices,
        borderColor: color,
        backgroundColor: color + '20',
        borderWidth: 2,
        pointRadius: 0,
        pointHoverRadius: 4,
        tension: 0.4,
        fill: true,
      }
    ]
  }
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      enabled: true,
      mode: 'index' as const,
      intersect: false,
      callbacks: {
        label: (context: any) => {
          return `₩${context.parsed.y.toLocaleString()}`
        }
      }
    }
  },
  scales: {
    x: { display: false },
    y: { display: false }
  },
  interaction: {
    mode: 'index' as const,
    intersect: false,
  }
}

// 상세 정보 표시
const showDetail = async (etf: ETF) => {
  try {
    // ETF 상세 정보 다시 가져오기 (investment_strategy와 top_holdings 포함)
    const response = await etfApi.getById(etf.id)
    selectedETF.value = response.data
    detailDialog.value = true
  } catch (err) {
    console.error('ETF 상세 정보 조회 실패:', err)
    // 에러 시 현재 데이터 사용
    selectedETF.value = etf
    detailDialog.value = true
  }
}

// 보유 비중 차트 옵션
const getHoldingsChartData = computed(() => {
  if (!selectedETF.value?.top_holdings || selectedETF.value.top_holdings.length === 0) {
    return null
  }

  const holdings = selectedETF.value.top_holdings
  const labels = holdings.map((h: any) => h.name)
  const data = holdings.map((h: any) => h.weight)
  const colors = [
    '#2196F3', '#4CAF50', '#FF9800', '#F44336', '#9C27B0',
    '#00BCD4', '#8BC34A', '#FF5722', '#673AB7', '#FFC107'
  ]

  return {
    labels,
    datasets: [{
      data,
      backgroundColor: colors.slice(0, holdings.length),
      borderWidth: 2,
      borderColor: '#fff'
    }]
  }
})

const holdingsChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right' as const,
      labels: {
        boxWidth: 12,
        padding: 10,
        font: { size: 11 }
      }
    },
    tooltip: {
      callbacks: {
        label: (context: any) => {
          return `${context.label}: ${context.parsed}%`
        }
      }
    }
  }
}

onMounted(() => {
  initializeColumns()
  fetchETFs()
})
</script>

<template>
  <v-card>
    <v-card-title class="d-flex justify-space-between align-center">
      <div>
        <span class="text-h5">배당 ETF 목록</span>
        <v-chip class="ml-3" color="primary" size="small">
          {{ etfs.length }}개
        </v-chip>
      </div>
      <div class="d-flex align-center ga-2">
        <v-btn
          icon="mdi-view-column"
          variant="text"
          size="small"
          @click="columnDialog = true"
          title="컬럼 설정"
        ></v-btn>
        <v-text-field
          v-model="search"
          density="compact"
          placeholder="검색 (티커, 이름, 섹터...)"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          hide-details
          single-line
          style="max-width: 400px"
        ></v-text-field>
      </div>
    </v-card-title>

    <v-card-text>
      <!-- 에러 메시지 -->
      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        <div class="font-weight-bold">API 호출 실패</div>
        <div>{{ error }}</div>
      </v-alert>

      <v-data-table
        :headers="headers"
        :items="etfs"
        :loading="loading"
        :search="search"
        :items-per-page="20"
        :items-per-page-options="[10, 20, 50, 100, { value: -1, title: '전체' }]"
        class="elevation-1"
        density="comfortable"
      >
        <!-- 티커 -->
        <template v-slot:item.ticker="{ item }">
          <span
            class="font-weight-bold text-primary cursor-pointer hover-underline"
            @click="showDetail(item)"
            style="cursor: pointer; text-decoration: underline;"
          >
            {{ item.ticker }}
          </span>
        </template>

        <!-- 이름 -->
        <template v-slot:item.name="{ item }">
          <div style="max-width: 300px; white-space: normal;">
            {{ item.name }}
          </div>
        </template>

        <!-- 가격 추이 미니 차트 -->
        <template v-slot:item.price_chart="{ item }">
          <div style="width: 120px; height: 40px;">
            <Line :data="getMiniChartOptions(item)" :options="chartOptions" />
          </div>
        </template>

        <!-- 현재가 -->
        <template v-slot:item.current_price="{ item }">
          <span class="font-weight-medium">{{ formatCurrency(item.current_price) }}</span>
        </template>

        <!-- 배당수익률 -->
        <template v-slot:item.dividend_yield="{ item }">
          <v-chip
            :color="getYieldColor(item.dividend_yield)"
            size="small"
            variant="flat"
          >
            {{ item.dividend_yield.toFixed(2) }}%
          </v-chip>
        </template>

        <!-- 일간 수익률 -->
        <template v-slot:item.return_1d="{ item }">
          <v-chip
            :color="formatPercent(item.return_1d).color"
            size="small"
            variant="tonal"
          >
            {{ formatPercent(item.return_1d).text }}
          </v-chip>
        </template>

        <!-- 주간 수익률 -->
        <template v-slot:item.return_1w="{ item }">
          <v-chip
            :color="formatPercent(item.return_1w).color"
            size="small"
            variant="tonal"
          >
            {{ formatPercent(item.return_1w).text }}
          </v-chip>
        </template>

        <!-- 월간 수익률 -->
        <template v-slot:item.return_1m="{ item }">
          <v-chip
            :color="formatPercent(item.return_1m).color"
            size="small"
            variant="tonal"
          >
            {{ formatPercent(item.return_1m).text }}
          </v-chip>
        </template>

        <!-- 연간 수익률 -->
        <template v-slot:item.return_1y="{ item }">
          <v-chip
            :color="formatPercent(item.return_1y).color"
            size="small"
            variant="flat"
          >
            {{ formatPercent(item.return_1y).text }}
          </v-chip>
        </template>

        <!-- 섹터 -->
        <template v-slot:item.sector="{ item }">
          <v-chip size="small" variant="outlined">
            {{ item.sector }}
          </v-chip>
        </template>

        <!-- 지역 -->
        <template v-slot:item.region="{ item }">
          <v-chip size="small" variant="outlined" color="secondary">
            {{ item.region }}
          </v-chip>
        </template>

        <!-- 비용 비율 -->
        <template v-slot:item.expense_ratio="{ item }">
          {{ item.expense_ratio.toFixed(2) }}%
        </template>

        <!-- 운용자산 -->
        <template v-slot:item.aum="{ item }">
          {{ item.aum.toLocaleString() }}억
        </template>

        <!-- 로딩 -->
        <template v-slot:loading>
          <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
        </template>

        <!-- 데이터 없음 -->
        <template v-slot:no-data>
          <v-alert type="info" variant="tonal" class="my-4">
            ETF 데이터가 없습니다.
          </v-alert>
        </template>

        <!-- 검색 결과 없음 -->
        <template v-slot:no-results>
          <v-alert type="warning" variant="tonal" class="my-4">
            "{{ search }}" 검색 결과가 없습니다.
          </v-alert>
        </template>

        <!-- 하단 페이지네이션 커스텀 -->
        <template v-slot:bottom>
          <div class="text-center pa-4">
            <v-pagination
              :length="Math.ceil(etfs.length / 20)"
              rounded="circle"
            ></v-pagination>
          </div>
        </template>
      </v-data-table>
    </v-card-text>

    <!-- 통계 요약 -->
    <v-card-text v-if="etfs.length > 0" class="pt-0">
      <v-divider class="mb-4"></v-divider>
      <v-row dense>
        <v-col cols="12" md="3">
          <v-card variant="tonal" color="primary">
            <v-card-text class="text-center">
              <div class="text-caption">평균 배당수익률</div>
              <div class="text-h6">
                {{ (etfs.reduce((sum, etf) => sum + etf.dividend_yield, 0) / etfs.length).toFixed(2) }}%
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card variant="tonal" color="success">
            <v-card-text class="text-center">
              <div class="text-caption">최고 배당수익률</div>
              <div class="text-h6">
                {{ Math.max(...etfs.map(e => e.dividend_yield)).toFixed(2) }}%
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card variant="tonal" color="info">
            <v-card-text class="text-center">
              <div class="text-caption">평균 연간수익률</div>
              <div class="text-h6">
                {{ (etfs.reduce((sum, etf) => sum + etf.return_1y, 0) / etfs.length).toFixed(2) }}%
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card variant="tonal" color="secondary">
            <v-card-text class="text-center">
              <div class="text-caption">총 운용자산</div>
              <div class="text-h6">
                {{ (etfs.reduce((sum, etf) => sum + etf.aum, 0) / 10000).toFixed(1) }}조
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>

    <!-- 컬럼 설정 다이얼로그 -->
    <v-dialog v-model="columnDialog" max-width="600">
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span>컬럼 표시 설정</span>
          <v-btn icon="mdi-close" variant="text" size="small" @click="columnDialog = false"></v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-4">
          <v-alert type="info" variant="tonal" density="compact" class="mb-4">
            표시할 컬럼을 선택하세요. 티커와 이름은 필수입니다.
          </v-alert>
          <v-list>
            <v-list-item
              v-for="header in allHeaders"
              :key="header.key"
              :disabled="header.required"
            >
              <template v-slot:prepend>
                <v-checkbox
                  v-model="selectedColumns"
                  :value="header.key"
                  :disabled="header.required"
                  hide-details
                ></v-checkbox>
              </template>
              <v-list-item-title>{{ header.title }}</v-list-item-title>
              <v-list-item-subtitle v-if="header.required">
                필수 컬럼
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="columnDialog = false">취소</v-btn>
          <v-btn color="primary" variant="flat" @click="saveColumns">저장</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ETF 상세 정보 다이얼로그 -->
    <v-dialog v-model="detailDialog" max-width="900">
      <v-card v-if="selectedETF">
        <v-card-title class="d-flex justify-space-between align-center bg-primary">
          <div>
            <div class="text-h5 font-weight-bold">{{ selectedETF.ticker }}</div>
            <div class="text-subtitle-2">{{ selectedETF.name }}</div>
          </div>
          <v-btn
            icon="mdi-close"
            variant="text"
            size="small"
            @click="detailDialog = false"
          ></v-btn>
        </v-card-title>

        <v-card-text class="pa-6">
          <!-- 주요 지표 -->
          <v-row class="mb-6">
            <v-col cols="6" md="3">
              <v-card variant="tonal" color="primary">
                <v-card-text class="text-center py-3">
                  <div class="text-caption text-grey">현재가</div>
                  <div class="text-h6 font-weight-bold">
                    {{ formatCurrency(selectedETF.current_price) }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="6" md="3">
              <v-card variant="tonal" color="success">
                <v-card-text class="text-center py-3">
                  <div class="text-caption text-grey">배당수익률</div>
                  <div class="text-h6 font-weight-bold">
                    {{ selectedETF.dividend_yield.toFixed(2) }}%
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="6" md="3">
              <v-card variant="tonal" color="info">
                <v-card-text class="text-center py-3">
                  <div class="text-caption text-grey">연간 수익률</div>
                  <div class="text-h6 font-weight-bold">
                    {{ formatPercent(selectedETF.return_1y).text }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="6" md="3">
              <v-card variant="tonal" color="secondary">
                <v-card-text class="text-center py-3">
                  <div class="text-caption text-grey">운용자산</div>
                  <div class="text-h6 font-weight-bold">
                    {{ selectedETF.aum.toLocaleString() }}억
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- 투자 전략 -->
          <div class="mb-6">
            <h3 class="text-h6 mb-3">
              <v-icon icon="mdi-strategy" size="small" class="mr-2"></v-icon>
              투자 전략
            </h3>
            <v-card variant="outlined">
              <v-card-text>
                <p v-if="selectedETF.investment_strategy" class="text-body-1">
                  {{ selectedETF.investment_strategy }}
                </p>
                <p v-else class="text-body-2 text-grey">
                  투자 전략 정보가 없습니다.
                </p>
              </v-card-text>
            </v-card>
          </div>

          <!-- 투자 비중 -->
          <div v-if="selectedETF.top_holdings && selectedETF.top_holdings.length > 0">
            <h3 class="text-h6 mb-3">
              <v-icon icon="mdi-chart-pie" size="small" class="mr-2"></v-icon>
              상위 보유 종목 (TOP 10)
            </h3>
            <v-row>
              <v-col cols="12" md="6">
                <div style="height: 300px;">
                  <Doughnut
                    v-if="getHoldingsChartData"
                    :data="getHoldingsChartData"
                    :options="holdingsChartOptions"
                  />
                </div>
              </v-col>
              <v-col cols="12" md="6">
                <v-list density="compact">
                  <v-list-item
                    v-for="(holding, index) in selectedETF.top_holdings"
                    :key="index"
                  >
                    <template v-slot:prepend>
                      <v-chip size="x-small" color="primary">{{ index + 1 }}</v-chip>
                    </template>
                    <v-list-item-title>{{ holding.name }}</v-list-item-title>
                    <template v-slot:append>
                      <v-chip size="small" variant="tonal">{{ holding.weight }}%</v-chip>
                    </template>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
          </div>
          <div v-else>
            <h3 class="text-h6 mb-3">
              <v-icon icon="mdi-chart-pie" size="small" class="mr-2"></v-icon>
              상위 보유 종목
            </h3>
            <v-alert type="info" variant="tonal">
              보유 종목 정보가 없습니다.
            </v-alert>
          </div>

          <!-- 추가 정보 -->
          <v-divider class="my-6"></v-divider>
          <v-row dense>
            <v-col cols="6" md="4">
              <div class="text-caption text-grey">섹터</div>
              <div class="text-body-1 font-weight-medium">{{ selectedETF.sector }}</div>
            </v-col>
            <v-col cols="6" md="4">
              <div class="text-caption text-grey">지역</div>
              <div class="text-body-1 font-weight-medium">{{ selectedETF.region }}</div>
            </v-col>
            <v-col cols="6" md="4">
              <div class="text-caption text-grey">비용비율</div>
              <div class="text-body-1 font-weight-medium">{{ selectedETF.expense_ratio.toFixed(2) }}%</div>
            </v-col>
            <v-col cols="6" md="4">
              <div class="text-caption text-grey">일간 수익률</div>
              <div class="text-body-1 font-weight-medium">{{ formatPercent(selectedETF.return_1d).text }}</div>
            </v-col>
            <v-col cols="6" md="4">
              <div class="text-caption text-grey">주간 수익률</div>
              <div class="text-body-1 font-weight-medium">{{ formatPercent(selectedETF.return_1w).text }}</div>
            </v-col>
            <v-col cols="6" md="4">
              <div class="text-caption text-grey">월간 수익률</div>
              <div class="text-body-1 font-weight-medium">{{ formatPercent(selectedETF.return_1m).text }}</div>
            </v-col>
          </v-row>
        </v-card-text>

        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="flat" @click="detailDialog = false">닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<style scoped>
:deep(.v-data-table) {
  font-size: 0.875rem;
}

:deep(.v-data-table__th) {
  font-weight: 600;
  background-color: rgba(var(--v-theme-primary), 0.05);
}

:deep(.v-data-table__td) {
  padding: 8px 16px !important;
}
</style>
