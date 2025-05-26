<!-- IncomeForm.vue -->
<template>
  <div class="form-wrapper">
    <p class="form-date">{{ date }}</p>

    <label>금액</label>
    <div class="input-icon-wrapper">
      <input type="number" v-model="amount" placeholder="금액 입력" />
      <span class="unit">₩</span>
      <span class="icon">💰</span>
    </div>

    <label>출처</label>
    <input list="sources" v-model="source" placeholder="출처 입력 또는 선택" />
    <datalist id="sources">
      <option value="월급" />
      <option value="용돈" />
      <option value="부수입" />
    </datalist>

    <label>감정</label>
    <div class="emotion-group">
      <span
        v-for="emo in emotions"
        :key="emo.value"
        :class="{ selected: emotion === emo.value }"
        @click="emotion = emo.value"
      >{{ emo.icon }}</span>
    </div>

    <div class="btn-group">
      <button class="cancel" @click="$emit('close')">닫기</button>
      <button class="submit" @click="handleSubmit">저장</button>
    </div>
  </div>
</template>

<script setup>
import { ref,watch } from 'vue'
import { useTransactionStore } from '@/stores/transactions'

const props = defineProps({ date: String })
const emit = defineEmits(['save', 'close'])

const store = useTransactionStore()

const amount = ref('')
const source = ref('')
const emotion = ref('')

const emotions = [
  { value: 'happy', icon: '😀' },
  { value: 'neutral', icon: '😐' },
  { value: 'sad', icon: '😟' },
]

async function handleSubmit() {
  if (!amount.value || !source.value) {
    alert('금액과 출처를 입력해주세요.')
    return
  }

  const payload = {
    date: props.date,
    amount: Math.abs(Number(amount.value)),
    source: source.value,
    emotion: emotion.value
  }

  await store.addIncome(payload)  // ✅ 수입 저장 (store에 addIncome 함수가 있어야 함)

  // ✅ 저장 직후 달력 갱신
  const dateObj = new Date(props.date)
  const year = dateObj.getFullYear()
  const month = dateObj.getMonth() + 1
  await store.fetchTransactions(year, month)

  // emit('close')
}

</script>

<style scoped>
.form-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-date {
  font-size: 16px;
  font-weight: 600;
  color: #555;
  margin-bottom: 1rem;
}

.input-icon-wrapper {
  position: relative;
}
.input-icon-wrapper input {
  width: 100%;
  padding: 0.6rem 2.5rem 0.6rem 0.6rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
}
.unit {
  position: absolute;
  right: 2rem;
  top: 50%;
  transform: translateY(-50%);
  font-weight: bold;
  color: #888;
}
.icon {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
}

.emotion-group {
  display: flex;
  gap: 1rem;
  font-size: 2rem;
}
.emotion-group span {
  cursor: pointer;
  transition: transform 0.1s ease;
}
.emotion-group span.selected {
  transform: scale(1.2);
  border-bottom: 2px solid #007bff;
}

.btn-group {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}
button.cancel {
  background: #ccc;
  color: black;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
button.submit {
  background: #007bff;
  color: white;
  padding: 0.5rem 1.2rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}</style>
