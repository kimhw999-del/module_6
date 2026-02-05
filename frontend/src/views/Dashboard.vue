<script setup lang="ts">
import { ref, onMounted, computed, markRaw } from 'vue'
import { useDraggable } from '@vueuse/core'
import DebugInfo from '@/components/DebugInfo.vue'
import ETFTable from '@/components/widgets/ETFTable.vue'
import PerformanceComparison from '@/components/widgets/PerformanceComparison.vue'
import ReturnRanking from '@/components/widgets/ReturnRanking.vue'
import PortfolioSummary from '@/components/widgets/PortfolioSummary.vue'
import DividendCalendar from '@/components/widgets/DividendCalendar.vue'
import SectorAllocation from '@/components/widgets/SectorAllocation.vue'

// 편집 모드
const editMode = ref(false)
const widgetDialog = ref(false)

// 위젯 정의
interface Widget {
  id: string
  name: string
  icon: string
  component: any
  visible: boolean
  order: number
}

const widgets = ref<Widget[]>([
  {
    id: 'debug',
    name: '디버그 정보',
    icon: 'mdi-bug',
    component: markRaw(DebugInfo),
    visible: true,
    order: 0
  },
  {
    id: 'return-ranking',
    name: '수익률 랭킹',
    icon: 'mdi-trophy',
    component: markRaw(ReturnRanking),
    visible: true,
    order: 1
  },
  {
    id: 'portfolio-summary',
    name: '포트폴리오 요약',
    icon: 'mdi-briefcase',
    component: markRaw(PortfolioSummary),
    visible: true,
    order: 2
  },
  {
    id: 'performance-comparison',
    name: '성과 비교',
    icon: 'mdi-chart-line-variant',
    component: markRaw(PerformanceComparison),
    visible: true,
    order: 3
  },
  {
    id: 'dividend-calendar',
    name: '배당 캘린더',
    icon: 'mdi-calendar',
    component: markRaw(DividendCalendar),
    visible: true,
    order: 4
  },
  {
    id: 'sector-allocation',
    name: '섹터/지역 분산',
    icon: 'mdi-chart-donut',
    component: markRaw(SectorAllocation),
    visible: true,
    order: 5
  },
  {
    id: 'etf-table',
    name: 'ETF 테이블',
    icon: 'mdi-table',
    component: markRaw(ETFTable),
    visible: true,
    order: 6
  }
])

// localStorage 키
const WIDGETS_KEY = 'dashboard-widgets-v2'

// 위젯 로드
const loadWidgets = () => {
  const saved = localStorage.getItem(WIDGETS_KEY)
  if (saved) {
    try {
      const savedWidgets = JSON.parse(saved)
      widgets.value.forEach(widget => {
        const savedWidget = savedWidgets.find((w: any) => w.id === widget.id)
        if (savedWidget) {
          widget.visible = savedWidget.visible
          widget.order = savedWidget.order
        }
      })
    } catch (e) {
      console.error('Failed to load widgets:', e)
    }
  }
}

// 위젯 저장
const saveWidgets = () => {
  const toSave = widgets.value.map(w => ({
    id: w.id,
    visible: w.visible,
    order: w.order
  }))
  localStorage.setItem(WIDGETS_KEY, JSON.stringify(toSave))
}

// 보이는 위젯
const visibleWidgets = computed(() => {
  return widgets.value
    .filter(w => w.visible)
    .sort((a, b) => a.order - b.order)
})

// 위젯 토글
const toggleWidget = (widgetId: string) => {
  const widget = widgets.value.find(w => w.id === widgetId)
  if (widget) {
    widget.visible = !widget.visible
    saveWidgets()
  }
}

// 레이아웃 리셋
const resetLayout = () => {
  if (confirm('대시보드를 기본 레이아웃으로 초기화하시겠습니까?')) {
    widgets.value.forEach((widget, index) => {
      widget.visible = true
      widget.order = index
    })
    saveWidgets()
  }
}

// 드래그 상태
const draggedWidget = ref<string | null>(null)

const onDragStart = (widgetId: string) => {
  if (!editMode.value) return
  draggedWidget.value = widgetId
}

const onDragOver = (e: DragEvent) => {
  e.preventDefault()
}

const onDrop = (targetWidgetId: string) => {
  if (!draggedWidget.value || draggedWidget.value === targetWidgetId) return

  const draggedIndex = widgets.value.findIndex(w => w.id === draggedWidget.value)
  const targetIndex = widgets.value.findIndex(w => w.id === targetWidgetId)

  if (draggedIndex !== -1 && targetIndex !== -1) {
    // 순서 교환
    const temp = widgets.value[draggedIndex].order
    widgets.value[draggedIndex].order = widgets.value[targetIndex].order
    widgets.value[targetIndex].order = temp

    saveWidgets()
  }

  draggedWidget.value = null
}

onMounted(() => {
  loadWidgets()
})
</script>

<template>
  <v-container fluid class="pa-4">
    <!-- 헤더 -->
    <div class="d-flex justify-space-between align-center mb-6">
      <h1 class="text-h4">
        <v-icon size="large" class="mr-2">mdi-chart-line</v-icon>
        배당 ETF 대시보드
      </h1>

      <div class="d-flex ga-2">
        <v-btn
          :color="editMode ? 'primary' : 'default'"
          :variant="editMode ? 'flat' : 'outlined'"
          @click="editMode = !editMode"
        >
          <v-icon start>{{ editMode ? 'mdi-check' : 'mdi-pencil' }}</v-icon>
          {{ editMode ? '완료' : '편집' }}
        </v-btn>

        <v-btn variant="outlined" @click="widgetDialog = true">
          <v-icon start>mdi-view-dashboard-edit</v-icon>
          위젯 관리
        </v-btn>

        <v-btn variant="text" icon="mdi-refresh" @click="resetLayout"></v-btn>
      </div>
    </div>

    <!-- 편집 모드 안내 -->
    <v-alert
      v-if="editMode"
      type="info"
      variant="tonal"
      density="compact"
      closable
      class="mb-4"
    >
      <v-icon start>mdi-information</v-icon>
      위젯을 드래그하여 순서를 변경할 수 있습니다.
    </v-alert>

    <!-- 위젯 그리드 -->
    <div class="widget-grid">
      <div
        v-for="widget in visibleWidgets"
        :key="widget.id"
        class="widget-item"
        :class="{ 'edit-mode': editMode, 'dragging': draggedWidget === widget.id }"
        :draggable="editMode"
        @dragstart="onDragStart(widget.id)"
        @dragover="onDragOver"
        @drop="onDrop(widget.id)"
      >
        <!-- 편집 모드 헤더 -->
        <div v-if="editMode" class="widget-header">
          <v-chip color="primary" size="small">
            <v-icon start size="small">mdi-drag</v-icon>
            <v-icon :icon="widget.icon" size="small" class="mx-1"></v-icon>
            {{ widget.name }}
          </v-chip>
        </div>

        <!-- 위젯 컴포넌트 -->
        <component :is="widget.component" />
      </div>
    </div>

    <!-- 위젯이 없을 때 -->
    <v-alert
      v-if="visibleWidgets.length === 0"
      type="info"
      variant="tonal"
      class="mt-4"
    >
      <v-icon start>mdi-information</v-icon>
      표시할 위젯이 없습니다. "위젯 관리"에서 위젯을 활성화하세요.
    </v-alert>

    <!-- 위젯 관리 다이얼로그 -->
    <v-dialog v-model="widgetDialog" max-width="600">
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span>위젯 관리</span>
          <v-btn
            icon="mdi-close"
            variant="text"
            size="small"
            @click="widgetDialog = false"
          ></v-btn>
        </v-card-title>

        <v-divider></v-divider>

        <v-card-text class="pa-4">
          <v-alert type="info" variant="tonal" density="compact" class="mb-4">
            위젯을 선택하여 대시보드에 표시하거나 숨길 수 있습니다.
          </v-alert>

          <v-list>
            <v-list-item v-for="widget in widgets" :key="widget.id">
              <template v-slot:prepend>
                <v-checkbox
                  v-model="widget.visible"
                  color="primary"
                  hide-details
                  @change="saveWidgets"
                ></v-checkbox>
              </template>

              <template v-slot:default>
                <div class="d-flex align-center">
                  <v-icon :icon="widget.icon" size="small" class="mr-2"></v-icon>
                  <v-list-item-title>{{ widget.name }}</v-list-item-title>
                </div>
              </template>

              <template v-slot:append>
                <v-chip
                  size="small"
                  :color="widget.visible ? 'success' : 'default'"
                  variant="tonal"
                >
                  {{ widget.visible ? '표시' : '숨김' }}
                </v-chip>
              </template>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn variant="text" @click="resetLayout">
            <v-icon start>mdi-refresh</v-icon>
            기본값으로 복원
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="flat" @click="widgetDialog = false">
            확인
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<style scoped>
.widget-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.widget-item {
  position: relative;
  transition: all 0.2s ease;
}

.widget-item.edit-mode {
  cursor: move;
  border: 2px dashed rgba(var(--v-theme-primary), 0.3);
  border-radius: 8px;
  padding: 8px;
}

.widget-item.edit-mode:hover {
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.2);
}

.widget-item.dragging {
  opacity: 0.5;
}

.widget-header {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 10;
  pointer-events: none;
}
</style>
