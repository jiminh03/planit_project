// stores/transactions.js
import { defineStore } from 'pinia'

export const useTransactionStore = defineStore('transaction', {
  state: () => ({
    transactions: []
  }),
  actions: {
    addTransaction(payload) {
      this.transactions.push(payload)
    },
    updateTransaction(index, updatedData) {
    console.log('[스토어 업데이트]', index, updatedData)
    this.transactions[index] = updatedData
},

    deleteTransaction(index) {
      this.transactions.splice(index, 1)
    }
  },
  getters: {
    getByDate: (state) => (date) =>
      state.transactions
        .map((t, i) => ({ ...t, _index: i })) // 수정/삭제용 인덱스 포함
        .filter(t => t.date === date)
  }
})
