<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { dividendApi } from '@/services/api'
import type { DividendCalendarItem } from '@/types'

const currentYear = new Date().getFullYear()
const currentMonth = new Date().getMonth() + 1

const selectedYear = ref(currentYear)
const selectedMonth = ref(currentMonth)
const dividends = ref<DividendCalendarItem[]>([])
const upcomingDividends = ref<DividendCalendarItem[]>([])
const loading = ref(false)
const viewMode = ref<'calendar' | 'upcoming'>('calendar')

const months = [
  { value: 1, label: '1월' },
  { value: 2, label: '2월' },
  { value: 3, label: '3월' },
  { value: 4, label: '4월' },
  { value: 5, label: '5월' },
  { value: 6, label: '6월' },
  { value: 7, label: '7월' },
  { value: 8, label: '8월' },
  { value: 9, label: '9월' },
  { value: 10, label: '10월' },
  { value: 11, label: '11월' },
  { value: 12, label: '12월' },
]

const years = computed(() => {
  const currentYear = new Date().getFullYear()
  return [currentYear - 1, currentYear, currentYear + 1]
})

const fetchDividends = async () => {
  loading.value = true
  try {
    const response = await dividendApi.getCalendar(selectedYear.value, selectedMonth.value)
    dividends.value = response.data
  } catch (error) {
    console.error('배당 캘린더 조회 실패:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return `${date.getMonth() + 1}/${date.getDate()}`
}

const frequencyLabel = (frequency: string) => {
  const labels: { [key: string]: string } = {
    monthly: '월배당',
    quarterly: '분기배당',
    annual: '연배당'
  }
  return labels[frequency] || frequency
}

const frequencyColor = (frequency: string) => {
  const colors: { [key: string]: string } = {
    monthly: 'success',
    quarterly: 'info',
    annual: 'warning'
  }
  return colors[frequency] || 'default'
}

const isUpcoming = (dateString: string) => {
  const today = new Date()
  const date = new Date(dateString)
  const diffDays = Math.ceil((date.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
  return diffDays >= 0 && diffDays <= 7
}

// 월별 통계
const monthlyStats = computed(() => {
  if (dividends.value.length === 0) return null

  const totalDividend = dividends.value.reduce((sum, d) => sum + d.dividend_per_share, 0)
  const avgYield = dividends.value
    .filter(d => d.dividend_yield)
    .reduce((sum, d) => sum + (d.dividend_yield || 0), 0) / dividends.value.length

  return {
    count: dividends.value.length,
    totalDividend: totalDividend.toFixed(0),
    avgYield: avgYield.toFixed(2)
  }
})

const fetchUpcoming = async () => {
  try {
    const response = await dividendApi.getUpcoming()
    upcomingDividends.value = response.data
  } catch (error) {
    console.error('다가오는 배당 조회 실패:', error)
  }
}

onMounted(() => {
  fetchDividends()
  fetchUpcoming()
})
</script>

<template>
  <v-card>
    <v-card-title class="d-flex justify-space-between align-center">
      <div>
        <v-icon class="mr-2">mdi-calendar-month</v-icon>
        배당 캘린더
      </div>
      <v-btn-toggle v-model="viewMode" mandatory density="compact" variant="outlined">
        <v-btn value="calendar" size="small">
          <v-icon>mdi-calendar</v-icon>
        </v-btn>
        <v-btn value="upcoming" size="small">
          <v-icon>mdi-bell-ring</v-icon>
        </v-btn>
      </v-btn-toggle>
    </v-card-title>

    <v-card-text>
      <div v-if="loading" class="text-center py-8">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <div class="text-caption mt-2">배당 일정 로딩 중...</div>
      </div>

      <!-- 월별 캘린더 뷰 -->
      <div v-else-if="viewMode === 'calendar'">
        <!-- 월/년 선택 -->
        <div class="d-flex gap-2 mb-4">
          <v-select
            v-model="selectedYear"
            :items="years"
            density="compact"
            style="max-width: 120px"
            hide-details
            variant="outlined"
            prepend-inner-icon="mdi-calendar"
            @update:model-value="fetchDividends"
          ></v-select>
          <v-select
            v-model="selectedMonth"
            :items="months"
            item-title="label"
            item-value="value"
            density="compact"
            style="max-width: 120px"
            hide-details
            variant="outlined"
            @update:model-value="fetchDividends"
          ></v-select>
        </div>

        <!-- 월별 통계 -->
        <v-card v-if="monthlyStats" variant="tonal" color="primary" class="mb-4">
          <v-card-text>
            <v-row dense>
              <v-col cols="4">
                <div class="text-caption text-grey">배당 건수</div>
                <div class="text-h6">{{ monthlyStats.count }}건</div>
              </v-col>
              <v-col cols="4">
                <div class="text-caption text-grey">평균 수익률</div>
                <div class="text-h6">{{ monthlyStats.avgYield }}%</div>
              </v-col>
              <v-col cols="4">
                <div class="text-caption text-grey">총 배당금</div>
                <div class="text-h6">{{ monthlyStats.totalDividend }}원</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <div v-if="dividends.length === 0" class="text-center py-8">
          <v-icon size="64" color="grey-lighten-1">mdi-calendar-remove</v-icon>
          <div class="text-h6 text-grey mt-3">선택한 기간에 배당 일정이 없습니다</div>
        </div>

        <v-timeline v-else side="end" density="compact" align="start">
          <v-timeline-item
            v-for="dividend in dividends"
            :key="dividend.id"
            :dot-color="isUpcoming(dividend.ex_dividend_date) ? 'success' : 'primary'"
            size="small"
          >
            <template v-slot:opposite>
              <div class="text-caption font-weight-bold">
                {{ formatDate(dividend.ex_dividend_date) }}
              </div>
            </template>

            <v-card
              :variant="isUpcoming(dividend.ex_dividend_date) ? 'elevated' : 'tonal'"
              :color="isUpcoming(dividend.ex_dividend_date) ? 'success' : undefined"
            >
              <v-card-text class="py-3">
                <div class="d-flex justify-space-between align-center mb-2">
                  <div>
                    <v-chip size="small" color="primary" variant="flat" class="font-weight-bold">
                      {{ dividend.ticker }}
                    </v-chip>
                    <v-chip
                      size="x-small"
                      :color="frequencyColor(dividend.frequency)"
                      variant="flat"
                      class="ml-2"
                    >
                      {{ frequencyLabel(dividend.frequency) }}
                    </v-chip>
                  </div>
                  <v-chip
                    v-if="isUpcoming(dividend.ex_dividend_date)"
                    size="x-small"
                    color="warning"
                    variant="flat"
                  >
                    <v-icon start size="x-small">mdi-bell-ring</v-icon>
                    임박
                  </v-chip>
                </div>
                <div class="text-body-2 mb-2">{{ dividend.name }}</div>
                <v-divider class="my-2"></v-divider>
                <v-row dense class="text-caption">
                  <v-col cols="6">
                    <v-icon size="small" class="mr-1">mdi-calendar-remove</v-icon>
                    배당락일: {{ formatDate(dividend.ex_dividend_date) }}
                  </v-col>
                  <v-col cols="6">
                    <v-icon size="small" class="mr-1">mdi-calendar-check</v-icon>
                    지급일: {{ formatDate(dividend.payment_date) }}
                  </v-col>
                </v-row>
                <div class="text-body-2 mt-2 font-weight-bold">
                  <v-icon size="small" class="mr-1">mdi-cash</v-icon>
                  주당 {{ dividend.dividend_per_share.toFixed(0) }}원
                  <span v-if="dividend.dividend_yield" class="text-primary ml-2">
                    (수익률 {{ dividend.dividend_yield.toFixed(2) }}%)
                  </span>
                </div>
              </v-card-text>
            </v-card>
          </v-timeline-item>
        </v-timeline>
      </div>

      <!-- 다가오는 배당 뷰 -->
      <div v-else-if="viewMode === 'upcoming'">
        <v-alert type="info" variant="tonal" density="compact" class="mb-4">
          <v-icon start>mdi-information</v-icon>
          향후 30일 이내 배당 일정
        </v-alert>

        <div v-if="upcomingDividends.length === 0" class="text-center py-8">
          <v-icon size="64" color="grey-lighten-1">mdi-calendar-clock</v-icon>
          <div class="text-h6 text-grey mt-3">다가오는 배당 일정이 없습니다</div>
        </div>

        <v-list v-else>
          <v-list-item
            v-for="dividend in upcomingDividends"
            :key="dividend.id"
            class="mb-2"
          >
            <template v-slot:prepend>
              <v-avatar :color="frequencyColor(dividend.frequency)" size="40">
                <span class="text-caption font-weight-bold">
                  {{ dividend.ticker.substring(0, 3) }}
                </span>
              </v-avatar>
            </template>

            <v-list-item-title class="font-weight-bold">
              {{ dividend.ticker }}
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ dividend.name }}
            </v-list-item-subtitle>

            <template v-slot:append>
              <div class="text-right">
                <div class="text-caption text-grey">배당락일</div>
                <div class="font-weight-bold">{{ formatDate(dividend.ex_dividend_date) }}</div>
                <v-chip size="x-small" color="success" variant="flat" class="mt-1">
                  {{ dividend.dividend_per_share.toFixed(0) }}원
                </v-chip>
              </div>
            </template>
          </v-list-item>
        </v-list>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
