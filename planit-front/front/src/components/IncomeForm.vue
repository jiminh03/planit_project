<template>
  <div class="form-wrapper">
    <p class="form-date">{{ date }}</p>

    <!-- 금액 입력 -->
    <label>금액</label>
    <div class="input-icon-wrapper">
      <input type="number" v-model="amount" placeholder="금액 입력" />
      <span class="unit">₩</span>
      <span class="icon">💰</span>
    </div>

    <!-- 수입 출처 -->
    <label>출처</label>
    <input list="sources" v-model="source" placeholder="출처 선택 또는 입력" />
    <datalist id="sources">
      <option value="월급" />
      <option value="용돈" />
      <option value="부수입" />
      <option value="기타" />
    </datalist>

    <!-- 감정 선택 -->
    <label>감정</label>
    <div class="emotion-group">
      <span
        v-for="emo in emotions"
        :key="emo.value"
        :class="{ selected: emotion === emo.value }"
        @click="emotion = emo.value"
      >{{ emo.icon }}</span>
    </div>

    <!-- 버튼 -->
    <div class="btn-group">
      <button class="cancel" @click="$emit('close')">취소</button>
      <button class="submit" @click="handleSubmit">저장</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  date: {
    type: String,
    editingItem: Object
  }
})

const emit = defineEmits(['save'])

const amount = ref('')
const source = ref('')
const emotion = ref('')

const emotions = [
  { value: 'happy', icon: '😀' },
  { value: 'neutral', icon: '😐' },
  { value: 'sad', icon: '😟' },
]

// onMounted(() => {
//   if (props.editingItem) {
//     amount.value = props.editingItem.amount
//     category.value = props.editingItem.category
//     emotion.value = props.editingItem.emotion
//   }
// })

function handleSubmit() {
  if (!amount.value || !source.value) {
    alert('금액과 출처를 입력해주세요.')
    return
  }

  const payload = {
    date: props.date,
    amount: Number(amount.value),
    source: source.value,
    emotion: emotion.value
  }

  console.log('💾 수입 저장 데이터:', payload)
  alert('수입이 저장되었습니다.')
  // emit('close')
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
}
</style>
