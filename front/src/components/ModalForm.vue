<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">
      <!-- ✅ 좌측: 오늘의 기록 리스트 -->
      <div class="modal-left">
        <h3>{{ date }}의 내역</h3>
        <!-- ✅ 수정 후: 수정 모드일 경우 input과 select로 대체 -->
        <div v-for="(item, idx) in todayList" :key="item._index" class="record-item">
          <!-- ✏️ 수정 모드일 경우 -->
          <template v-if="editingItem && editingItem._index === item._index">
            <input type="number" v-model="editingItem.amount" style="width: 80px;" />
            <input type="text" v-model="editingItem.category" style="width: 80px;" />
            <select v-model="editingItem.emotion">
              <option value="happy">😀</option>
              <option value="neutral">😐</option>
              <option value="sad">😟</option>
            </select>
            <button @click="saveEdit(editingItem)">저장</button>
            <button @click="cancelEdit">취소</button>
          </template>

          <!-- 👀 기본 보기 모드 -->
          <template v-else>
            <div class="cell amount" :class="item.amount > 0 ? 'income' : 'expense'">
              {{ item.amount.toLocaleString() }}원
            </div>
            <div class="cell">{{ item.category || item.source }}</div>
            <div class="cell emoji">{{ emojiMap[item.emotion] }}</div>
            <div class="cell action-buttons">
              <button @click="editItem(item)">✏️</button>
              <button @click="deleteItem(item._index)">❌</button>
            </div>
          </template>
        </div>

      </div>
      <!-- ✅ 우측: 탭 + 폼 입력 -->
      <div class="modal-right">
        <div class="tabs">
          <span :class="{ active: tab === 'expense' }" @click="tab = 'expense'">지출</span>
          <span :class="{ active: tab === 'income' }" @click="tab = 'income'">수입</span>
        </div>

        <component :is="tabMap[tab]" :date="date" :editing="editingItem" @save="handleSave" @close="$emit('close')" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTransactionStore } from '@/stores/transactions'
import ExpenseForm from './ExpenseForm.vue'
import IncomeForm from './IncomeForm.vue'
import { forceUpdate } from '@/stores/summaryTrigger'

const props = defineProps({ date: String })
const tab = ref('expense')
const tabMap = { expense: ExpenseForm, income: IncomeForm }

const store = useTransactionStore()

const todayList = computed(() => store.getByDate(props.date))

const emojiMap = {
  happy: '😀',
  neutral: '😐',
  sad: '😟'
}
const editingItem = ref(null)

function handleEdit(item) {
  editingItem.value = item
}
const emit = defineEmits(['edit'])

function editItem(item) {
  editingItem.value = { ...item }
  tab.value = item.amount > 0 ? 'income' : 'expense'
  // emit('edit', item)  // 폼에 데이터 전달
}

function deleteItem(index) {
  if (confirm('정말 삭제하시겠습니까?')) {
    store.deleteTransaction(index)
  }
}

function saveEdit(item) {
  const newItem = { ...item }  // ✅ 새 객체로 복사하여 반응성 보장
  store.updateTransaction(newItem._index, newItem)
  editingItem.value = null
}

async function handleSave(data) {
  if (data._index !== undefined && data._index !== null) {
    store.updateTransaction(data._index, data)
  } else {
    if (data.amount > 0) {
      store.addIncome(data)
    } else {
      store.addExpense(data)
    }
    const dateObj = new Date(props.date)
    const year = dateObj.getFullYear()
    const month = dateObj.getMonth() + 1
    await store.fetchTransactions(year, month)
    forceUpdate.value = !forceUpdate.value
  }
  editingItem.value = null
}

function cancelEdit() {
  editingItem.value = null   // ✅ 수정 모드 종료
}


</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(66, 66, 66, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-container {
  display: flex;
  background: white;
  width: 800px;
  height: 500px;
  border-radius: 16px;
  overflow: hidden;
}

.modal-left {
  width: 50%;
  background: #f0f0f0;
  padding: 1rem;
  overflow-y: auto;
}

/* Record item grid style for better alignment */
.record-item {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0;
  border-bottom: 1px solid #ccc;
  font-size: 14px;
}

.cell {
  display: flex;
  align-items: center;
}

.amount {
  font-weight: bold;
}

.income {
  color: blue;
}

.expense {
  color: red;
}

.action-buttons {
  display: flex;
  gap: 0.4rem;
}

.modal-right {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 1rem;
}

.tabs span {
  cursor: pointer;
  padding-bottom: 4px;
  border-bottom: 2px solid transparent;
}

.tabs .active {
  font-weight: bold;
  border-color: #007bff;
}

.action-buttons button {
  background-color: #ffffff00;  /* ✅ 밝은 회색 */
  color: black;
  border: none;
  border-radius: 6px;
  padding: 0.4rem 0.6rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.action-buttons button:hover {
  background-color: #e0e0e0; /* 🔆 hover 시 더 진한 회색 */
}

</style>
