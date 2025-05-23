<!-- ExpenseForm.vue -->
<template>
  <div class="form-wrapper">
    <p class="form-date">{{ date }}</p>

    <label>금액</label>
    <div class="input-icon-wrapper">
      <input type="number" v-model="amount" placeholder="금액 입력" />
      <span class="unit">₩</span>
      <span class="icon">🧾</span>
    </div>

    <label>카테고리</label>
    <input list="categories" v-model="category" placeholder="카테고리 선택" />
    <datalist id="categories">
      <option value="식비" />
      <option value="교통" />
      <option value="문화생활" />
      <option value="쇼핑" />
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
import { ref, watch } from 'vue'
import { useTransactionStore } from '@/stores/transactions'

const props = defineProps({ date: String })
const emit = defineEmits(['save', 'close'])
const index = ref(null)

const store = useTransactionStore()

const amount = ref('')
const category = ref('')
const emotion = ref('')

const emotions = [
  { value: 'happy', icon: '😀' },
  { value: 'neutral', icon: '😐' },
  { value: 'sad', icon: '😟' },
]

watch(() => props.editing, (item) => {
  if (item) {
    amount.value = Math.abs(item.amount)
    emotion.value = item.emotion
    category.value = item.category || ''
    // source.value = item.source || ''
    index.value = item._index   // ✅ 여기 매우 중요
  } else {
    amount.value = ''
    category.value = ''
    // source.value = ''
    emotion.value = ''
    index.value = null
  }
}, { immediate: true })


function handleSubmit() {
  if (!amount.value || !category.value) {
    alert('금액과 카테고리를 입력해주세요.')
    return
  }

  const payload = {
  date: props.date,
  amount: -Math.abs(Number(amount.value)),  // 또는 +amount
  category: category.value,
  emotion: emotion.value,
  // source: source.value,
  _index: index.value   // ✅ 이게 빠져있으면 update 못함
}

emit('save', payload)


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
